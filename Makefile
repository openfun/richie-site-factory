# -- Docker
DOCKER_UID           = $(shell id -u)
DOCKER_GID           = $(shell id -g)
COMPOSE              = DOCKER_USER="$(DOCKER_UID):$(DOCKER_GID)" docker-compose
COMPOSE_RUN          = $(COMPOSE) run --rm
COMPOSE_EXEC         = $(COMPOSE) exec
COMPOSE_EXEC_APP     = $(COMPOSE_EXEC) app
COMPOSE_EXEC_CI      = $(COMPOSE_EXEC) app-ci
COMPOSE_EXEC_LMS     = $(COMPOSE_EXEC) lms
COMPOSE_TEST_RUN     = $(COMPOSE_RUN) -e DJANGO_CONFIGURATION=Test
COMPOSE_TEST_RUN_APP = $(COMPOSE_TEST_RUN) app

# -- Node

# We must run node with a /home because yarn tries to write to ~/.yarnrc. If the
# ID of our host user (with which we run the container) does not exist in the
# container (e.g. 1000 exists but 1009 does not exist by default), then yarn
# will try to write to "/.yarnrc" at the root of the system and will fail with a
# permission error.
COMPOSE_RUN_NODE     = $(COMPOSE_RUN) -e HOME="/tmp" node
YARN                 = $(COMPOSE_RUN_NODE) yarn

# -- Django
MANAGE = $(COMPOSE_EXEC_APP) python manage.py
MANAGE_CI = $(COMPOSE_EXEC_CI) python manage.py
MANAGE_LMS = $(COMPOSE_EXEC_LMS) python manage.py lms

# -- Rules
default: help

bootstrap: \
  env.d/aws \
  data/media/.keep \
  data/static/.keep \
  build-front \
  build \
  run \
  migrate \
  init
bootstrap: ## install development dependencies
.PHONY: bootstrap

# == Docker
build: ## build the app container
	$(COMPOSE) build app
.PHONY: build

down: ## stop & remove containers
	@$(COMPOSE) down
.PHONY: down

logs: ## display app logs (follow mode)
	@$(COMPOSE) logs -f app
.PHONY: logs

run: ## start the wsgi (production) or development server
	@$(COMPOSE) up -d app
	@echo "Wait for services to be up..."
	$(COMPOSE_RUN) dockerize -wait tcp://postgresql:5432 -timeout 60s
	$(COMPOSE_RUN) dockerize -wait tcp://elasticsearch:9200 -timeout 60s
.PHONY: run

stop: ## stop the development server
	@$(COMPOSE) stop
.PHONY: stop

# == Frontend
build-front: \
  install-front \
  build-sass
build-front: ## build front-end application
.PHONY: build-front

build-sass: ## build Sass files to CSS
	@$(YARN) sass
.PHONY: build-sass

build-sass-production: ## build Sass files to CSS (production mode)
	@$(YARN) sass-production
.PHONY: build-sass-production

install-front: ## install front-end dependencies
	@$(YARN) install
.PHONY: install-front

install-front-production: ## install front-end dependencies (production mode)
	@$(YARN) install --frozen-lockfile
.PHONY: install-front-production

lint-front-prettier: ## run prettier linter over scss files
	@$(YARN) prettier
.PHONY: lint-front-prettier

lint-front-prettier-write: ## run prettier over scss files -- beware! overwrites files
	@$(YARN) prettier-write
.PHONY: lint-front-prettier-write

watch-sass: ## watch changes in Sass files
	@$(YARN) watch-sass
.PHONY: watch-sass

# == AWS/Terraform
env.d/aws:
	cp env.d/aws.dist env.d/aws

# == Django
check: \
  run
check: ## perform django checks
	@$(MANAGE) check
.PHONY: check

collectstatic: \
  run
collectstatic: ## collect static files to /data/static
	@$(MANAGE) collectstatic
.PHONY: collectstatic

init: \
  run
init: ## create base site structure
	@$(MANAGE) richie_init
	@${MAKE} search-index
.PHONY: init

# Nota bene: Black should come after isort just in case they don't agree...
lint-back: ## lint back-end python sources
lint-back: \
  lint-back-isort \
  lint-back-black \
  lint-back-flake8 \
  lint-back-pylint \
  lint-back-bandit
.PHONY: lint-back

lint-back-black: ## lint back-end python sources with black
	@echo 'lint:black started…'
	@$(COMPOSE_TEST_RUN_APP) black .
.PHONY: lint-back-black

lint-back-flake8: ## lint back-end python sources with flake8
	@echo 'lint:flake8 started…'
	@$(COMPOSE_TEST_RUN_APP) flake8
.PHONY: lint-back-flake8

lint-back-isort: ## automatically re-arrange python imports in back-end code base
	@echo 'lint:isort started…'
	@$(COMPOSE_TEST_RUN_APP) isort --recursive --atomic .
.PHONY: lint-back-isort

lint-back-pylint: ## lint back-end python sources with pylint
	@echo 'lint:pylint started…'
	@$(COMPOSE_TEST_RUN_APP) pylint .
.PHONY: lint-back-pylint

lint-back-bandit: ## lint back-end python sources with bandit
	@echo 'lint:bandit started…'
	@$(COMPOSE_TEST_RUN_APP) bandit -qr .
.PHONY: lint-back-bandit

migrate: \
  run
migrate: ## perform database migrations
	@$(MANAGE) migrate
.PHONY: migrate

search-index: \
  run
search-index: ## (re)generate the Elasticsearch index
	@$(MANAGE) bootstrap_elasticsearch
.PHONY: search-index

superuser: \
  run
superuser: ## create a DjangoCMS superuser
	@$(MANAGE) createsuperuser
.PHONY: superuser

# == CI
ci-build: ## build the app production container in the CI
	$(COMPOSE) build app-ci
.PHONY: ci-build

ci-check: \
  ci-run
ci-check: ## run django check management command
	$(MANAGE_CI) check
.PHONY: ci-check

ci-migrate: \
  ci-run
ci-migrate: ## perform database migrations in the CI
	$(MANAGE_CI) migrate
.PHONY: ci-migrate

ci-run: ## start the wsgi server (and linked services)
	@$(COMPOSE) up -d app-ci
	# As we use a remote docker environment, we should explicitly use the same
	# network to check containers status
	@echo "Wait for services to be up..."
	$(COMPOSE_RUN) dockerize -wait tcp://postgresql:5432 -timeout 60s
	$(COMPOSE_RUN) dockerize -wait tcp://elasticsearch:9200 -timeout 60s
.PHONY: ci-run

ci-version: ## check version file bundled in the docker image
	$(COMPOSE_RUN) --no-deps app-ci cat version.json
.PHONY: ci-version

# == edxapp
lms-bootstrap: \
  lms-run \
  lms-migrate \
  lms-sso \
  lms-collectstatic
lms-bootstrap: ## install edxapp LMS
.PHONY: lms-bootstrap

lms-collectstatic: \
  lms-run \
  data/edx/static/.keep
lms-collectstatic: ## copy static assets to LMS static root directory
	$(COMPOSE_EXEC) collectstatic --noinput --settings=fun.docker_run_development
.PHONY: lms-collectstatic

lms-sso: \
  lms-run \
  lms-migrate
lms-sso: ## generate SSO client application token
	$(COMPOSE_EXEC_LMS) python /usr/local/bin/create_oauth_client
.PHONY: lms-sso

lms-logs: ## display lms logs (follow mode)
	@$(COMPOSE) logs -f lms
.PHONY: lms-logs

lms-migrate: \
  lms-run \
  data/edx/media/.keep
lms-migrate: ## perform LMS database migration
	$(MANAGE_LMS) migrate
.PHONY: lms-migrate

lms-run:\
  data/edx/data/.keep
lms-run: ## run openedx lms (auth provider)
	$(COMPOSE) up -d lms
	$(COMPOSE_RUN) dockerize -wait tcp://mysql:3306 -timeout 60s
.PHONY: lms-run

# == Misc
clean: ## restore repository state as it was freshly cloned
	git clean -idx
.PHONY: clean

data/media/.keep:
	@echo 'Preparing media volume...'
	@mkdir -p data/media
	@touch data/media/.keep

data/static/.keep:
	@echo 'Preparing static volume...'
	@mkdir -p data/static
	@touch data/static/.keep

data/edx/data/.keep:
	@echo 'Preparing edx data volume...'
	@mkdir -p data/edx/data
	@touch data/edx/data/.keep

data/edx/media/.keep:
	@echo 'Preparing edx media volume...'
	@mkdir -p data/edx/media
	@touch data/edx/media/.keep

data/edx/static/.keep:
	@echo 'Preparing edx static volume...'
	@mkdir -p data/edx/static
	@touch data/edx/static/.keep

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
