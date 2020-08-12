RICHIE_SITE ?= funmooc

# -- Terminal colors
COLOR_INFO    = \033[0;36m
COLOR_RESET   = \033[0m

# -- Docker
DOCKER_UID           = $(shell id -u)
DOCKER_GID           = $(shell id -g)
NGINX_IMAGE_NAME     = fundocker/openshift-nginx
NGINX_IMAGE_TAG      = 1.13

COMPOSE              = \
  NGINX_IMAGE_NAME="$(NGINX_IMAGE_NAME)" \
  NGINX_IMAGE_TAG="$(NGINX_IMAGE_TAG)" \
  DOCKER_USER="$(DOCKER_UID):$(DOCKER_GID)" \
  docker-compose
COMPOSE_RUN          = $(COMPOSE) run --rm
COMPOSE_RUN_APP      = $(COMPOSE_RUN) app-dev
COMPOSE_EXEC         = $(COMPOSE) exec
COMPOSE_EXEC_APP     = $(COMPOSE_EXEC) app-dev
COMPOSE_TEST_RUN     = $(COMPOSE) run --rm -e DJANGO_CONFIGURATION=Test
COMPOSE_TEST_RUN_APP = $(COMPOSE_TEST_RUN) app-dev
WAIT_DB              = $(COMPOSE_RUN) dockerize -wait tcp://db:5432 -timeout 60s
WAIT_ES              = $(COMPOSE_RUN) dockerize -wait tcp://elasticsearch:9200 -timeout 60s
WAIT_SENTINEL        = $(COMPOSE_RUN) dockerize -wait tcp://redis-sentinel:26379 -wait tcp://redis-primary:6379 -timeout 20s

# -- Node

# We must run node with a /home because yarn tries to write to ~/.yarnrc. If the
# ID of our host user (with which we run the container) does not exist in the
# container (e.g. 1000 exists but 1009 does not exist by default), then yarn
# will try to write to "/.yarnrc" at the root of the system and will fail with a
# permission error.
COMPOSE_RUN_NODE     = $(COMPOSE_RUN) -e HOME="/tmp" node
YARN                 = $(COMPOSE_RUN_NODE) yarn

# -- Django
MANAGE = $(COMPOSE_RUN_APP) python manage.py

# -- Rules
default: help

bootstrap: \
  env.d/aws \
  data/media/$(RICHIE_SITE)/.keep \
  data/db/$(RICHIE_SITE) \
  stop \
  build-front \
  build \
  run \
  migrate \
  init
bootstrap:  ## install development dependencies
.PHONY: bootstrap

# == Docker
build: ## build all containers
	$(COMPOSE) build app
	$(COMPOSE) build nginx
	$(COMPOSE) build app-dev
.PHONY: build

reset:  ## Remove database and local files
	$(COMPOSE) stop
	rm -Ir data/* || exit 0
	$(COMPOSE) rm db
.PHONY: reset

down: ## stop & remove containers
	@$(COMPOSE) down
.PHONY: down

logs: ## display app logs (follow mode)
	@$(COMPOSE) logs -f app-dev
.PHONY: logs

run: ## start the wsgi (production) or development server
	@$(COMPOSE) up -V -d redis-sentinel
	@$(WAIT_SENTINEL)
	@$(COMPOSE) up -d nginx
	@$(COMPOSE) up -d app-dev
	@$(WAIT_DB)
.PHONY: run

stop: ## stop the development server
	@$(COMPOSE) stop
.PHONY: stop

info:  ## get activated site info
	@echo "RICHIE_SITE: $(COLOR_INFO)$(RICHIE_SITE)$(COLOR_RESET)"
.PHONY: info

# == Frontend
build-front: install-front build-sass ## build front-end application
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

test-back: ## run back-end tests
	bin/pytest
.PHONY: test-back

watch-sass: ## watch changes in Sass files
	@$(YARN) watch-sass
.PHONY: watch-sass

# == AWS/Terraform
env.d/aws:
	cp env.d/aws.dist env.d/aws

# == Django
check: ## perform django checks
	@$(MANAGE) check
.PHONY: check

demo-site: ## create a demo site
	@$(COMPOSE) up -d db
	@$(WAIT_DB)
	@$(MANAGE) flush
	@$(MANAGE) create_demo_site
	@${MAKE} search-index
.PHONY: demo-site

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

import-fixtures:  ## import fixtures
	@$(MANAGE) import_fixtures -v3
.PHONY: import-fixtures

messages: ## create the .po files used for i18n
	@$(MANAGE) makemessages --keep-pot
.PHONY: messages

migrate: ## perform database migrations
	@$(COMPOSE) up -d db
	@$(WAIT_DB)
	@$(MANAGE) migrate
.PHONY: migrate

search-index: ## (re)generate the Elasticsearch index
	@$(COMPOSE) up -d elasticsearch
	@$(WAIT_ES)
	@$(MANAGE) bootstrap_elasticsearch
.PHONY: search-index

superuser: ## create a DjangoCMS superuser
	@$(COMPOSE) up -d db
	@$(WAIT_DB)
	@$(MANAGE) createsuperuser
.PHONY: superuser

# == CI
ci-check: ## run django check management command on productin image
	$(COMPOSE_RUN) app python manage.py check
.PHONY: ci-check

ci-migrate: ## run django migrate command on production image
	@$(COMPOSE) up -d db
	@$(WAIT_DB)
	$(COMPOSE_RUN) app python manage.py migrate
.PHONY: ci-migrate

ci-run: ## start the wsgi server (and linked services)
	@$(COMPOSE) up -d app
	# As we use a remote docker environment, we should explicitly use the same
	# network to check containers status
	@echo "Wait for services to be up..."
	docker run --network container:fun_db_1 --rm jwilder/dockerize -wait tcp://localhost:5432 -timeout 60s
	docker run --network container:fun_elasticsearch_1 --rm jwilder/dockerize -wait tcp://localhost:9200 -timeout 60s
.PHONY: ci-run

ci-version: ## check version file bundled in the docker image
	$(COMPOSE_RUN) --no-deps app cat version.json
.PHONY: ci-version

# == Misc
clean: ## restore repository state as it was freshly cloned
	git clean -idx
.PHONY: clean

data/media/$(RICHIE_SITE)/.keep:
	@echo 'Preparing media volume...'
	@mkdir -p data/media/$(RICHIE_SITE)
	@touch data/media/$(RICHIE_SITE)/.keep

data/db/$(RICHIE_SITE):
	@echo 'Preparing db volume...'
	@mkdir -p data/db/$(RICHIE_SITE)

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
