# -- Docker
UID              = $(shell id -u)
GID              = $(shell id -g)
COMPOSE          = UID="$(UID):$(GID)" docker-compose
COMPOSE_RUN      = $(COMPOSE) run --rm
COMPOSE_RUN_APP  = $(COMPOSE_RUN) app
COMPOSE_EXEC     = $(COMPOSE) exec
COMPOSE_EXEC_APP = $(COMPOSE_EXEC) app

# -- Node

# We must run node with a /home because yarn tries to write to ~/.yarnrc. If the
# ID of our host user (with which we run the container) does not exist in the
# container (e.g. 1000 exists but 1009 does not exist by default), then yarn
# will try to write to "/.yarnrc" at the root of the system and will fail with a
# permission error.
COMPOSE_RUN_NODE     = $(COMPOSE_RUN) -e HOME="/tmp" node
YARN                 = $(COMPOSE_RUN_NODE) yarn

# -- Django
ifeq ($(BUILD_TARGET), production)
	MANAGE = $(COMPOSE_RUN_APP) python manage.py
else
	MANAGE = $(COMPOSE_RUN_APP) dockerize -wait tcp://db:5432 -timeout 60s \
		python manage.py
endif

# -- Rules
default: help

bootstrap: data/media/.keep data/static/.keep build-front build run migrate  ## install development dependencies
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
	@$(COMPOSE) up -d
.PHONY: run

stop: ## stop the development server
	@$(COMPOSE) stop
.PHONY: stop

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

watch-sass: ## watch changes in Sass files
	@$(YARN) watch-sass
.PHONY: watch-sass

# == Django tasks
check:  ## perform django checks
	@$(MANAGE) check
.PHONY: check

demo-site:  ## create a demo site
	@$(MANAGE) flush
	@$(MANAGE) create_demo_site
	@${MAKE} search-index;
.PHONY: demo-site

migrate:  ## perform database migrations
	@$(MANAGE) migrate
.PHONY: migrate

search-index:  ## (re)generate the Elasticsearch index
	@$(MANAGE) bootstrap_elasticsearch
.PHONY: search-index

superuser: ## create a DjangoCMS superuser
	@$(MANAGE) createsuperuser
.PHONY: superuser

# == Misc
clean: ## restore repository state as it was freshly cloned
	git clean -idx
.PHONY: clean

data/media/.keep:
	@echo 'Preparing media volume...'
	@mkdir -p data/media/.keep

data/static/.keep:
	@echo 'Preparing static volume...'
	@mkdir -p data/media/.keep

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
