# -- Docker
UID              = $(shell id -u)
COMPOSE          = docker-compose
COMPOSE_RUN      = $(COMPOSE) run --rm
COMPOSE_RUN_APP  = $(COMPOSE_RUN) app
COMPOSE_EXEC     = $(COMPOSE) exec
COMPOSE_EXEC_APP = $(COMPOSE_EXEC) app

# -- Django
ifeq ($(BUILD_TARGET), production)
	MANAGE = $(COMPOSE_RUN_APP) python manage.py
else
	MANAGE = $(COMPOSE_RUN_APP) dockerize -wait tcp://db:5432 -timeout 60s \
		python manage.py
endif

# -- Rules
default: help

bootstrap: data/media/.keep data/static/.keep build run migrate  ## install development dependencies
.PHONY: bootstrap

# == Docker
build: ## build the app container
	@$(COMPOSE) build --build-arg UID=$(UID) app
.PHONY: build

down: ## stop & remove containers
	@$(COMPOSE) down
.PHONY: down

logs: ## display app logs (follow mode)
	@$(COMPOSE) logs -f app
.PHONY: logs

run: ## start the development server
	@$(COMPOSE) up -d
.PHONY: run

stop: ## stop the development server
	@$(COMPOSE) stop
.PHONY: stop

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
