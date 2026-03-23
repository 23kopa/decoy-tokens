
# VARIABLES
DOCKER_COMPOSE = docker compose

APP_BACKEND = backend
APP_FRONTEND = frontend


# DEVELOPMENT
.PHONY: up
up:
	$(DOCKER_COMPOSE) up -d

.PHONY: up-build
up-build:
	$(DOCKER_COMPOSE) up --build

.PHONY: down
down:
	$(DOCKER_COMPOSE) down

.PHONY: logs
logs:
	$(DOCKER_COMPOSE) logs -f $(APP_BACKEND)

.PHONY: restart
restart:
	$(DOCKER_COMPOSE) down
	$(DOCKER_COMPOSE) up -d

# BACKEND
.PHONY: back-shell
back-shell:
	$(DOCKER_COMPOSE) exec $(APP_BACKEND) /bin/sh

.PHONY: back-restart
back-restart:
	$(DOCKER_COMPOSE) restart $(APP_BACKEND)

# DATABASE
.PHONY: migrate
migrate:
	$(DOCKER_COMPOSE) exec $(APP_BACKEND) alembic upgrade head

.PHONY: makemigration
makemigration:
	$(DOCKER_COMPOSE) exec $(APP_BACKEND) alembic revision --autogenerate -m "$(name)"

.PHONY: downgrade
downgrade:
	$(DOCKER_COMPOSE) exec $(APP_BACKEND) alembic downgrade -1

# FRONTEND
.PHONY: front-dev
front-dev:
	cd $(APP_FRONTEND) && npm run dev

.PHONY: front-build
front-build:
	cd $(APP_FRONTEND) && npm run build

.PHONY: front-install
front-install:
	cd $(APP_FRONTEND) && npm install

# QUALITY / FORMATTING
.PHONY: lint
lint:
	$(DOCKER_COMPOSE) exec $(APP_BACKEND) ruff check .

.PHONY: format
format:
	$(DOCKER_COMPOSE) exec $(APP_BACKEND) ruff format .

# UTILITIES
.PHONY: ps
ps:
	$(DOCKER_COMPOSE) ps

.PHONY: clean
clean:
	$(DOCKER_COMPOSE) down -v

# TESTS INSIDE DOCKER
.PHONY: test
test:
	$(DOCKER_COMPOSE) exec $(APP_BACKEND) pytest backend/tests/ -v

.PHONY: test-unit
test-unit:
	$(DOCKER_COMPOSE) exec $(APP_BACKEND) pytest backend/tests/unit/ -v

.PHONY: test-ip
test-ip:
	$(DOCKER_COMPOSE) exec $(APP_BACKEND) pytest backend/tests/unit/services/decoy_tokens/utils/ip/ -v

.PHONY: test-geo
test-geo:
	$(DOCKER_COMPOSE) exec $(APP_BACKEND) pytest backend/tests/unit/services/decoy_tokens/utils/geo/ -v	