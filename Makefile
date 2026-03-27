# --------------------
# CONFIG
# --------------------
COMPOSE_DEV = docker compose
COMPOSE_PROD = docker compose -f docker-compose.prod.yml

BACKEND = backend
FRONTEND = frontend

.PHONY: help

help:
	@echo "Available targets:"
	@echo "  dev-up / dev-down / dev-restart / dev-logs / dev-ps"
	@echo "  dev-shell / dev-migrate / dev-test"
	@echo "  prod-up / prod-down / prod-restart / prod-logs / prod-ps"
	@echo "  prod-migrate / prod-deploy / prod-status"


# --------------------
# DEV LIFECYCLE
# --------------------
.PHONY: dev-up dev-down dev-restart dev-logs dev-ps dev-shell

dev-up:
	$(COMPOSE_DEV) up -d

dev-down:
	$(COMPOSE_DEV) down

dev-restart:
	$(COMPOSE_DEV) down && $(COMPOSE_DEV) up -d

dev-logs:
	$(COMPOSE_DEV) logs -f $(BACKEND)

dev-ps:
	$(COMPOSE_DEV) ps

dev-shell:
	$(COMPOSE_DEV) exec $(BACKEND) /bin/sh


# --------------------
# DEV DATABASE
# --------------------
.PHONY: dev-migrate dev-makemigration dev-downgrade

dev-migrate:
	$(COMPOSE_DEV) exec $(BACKEND) alembic upgrade head

dev-makemigration:
	$(COMPOSE_DEV) exec $(BACKEND) alembic revision --autogenerate -m "$(name)"

dev-downgrade:
	$(COMPOSE_DEV) exec $(BACKEND) alembic downgrade -1


# --------------------
# DEV FRONTEND
# --------------------
.PHONY: dev-front dev-front-build dev-front-install

dev-front:
	cd $(FRONTEND) && npm run dev

dev-front-build:
	cd $(FRONTEND) && npm run build

dev-front-install:
	cd $(FRONTEND) && npm install


# --------------------
# TESTS
# --------------------
.PHONY: dev-test

dev-test:
	$(COMPOSE_DEV) exec $(BACKEND) pytest -v


# --------------------
# PROD LIFECYCLE
# --------------------
.PHONY: prod-up prod-down prod-restart prod-rebuild prod-upgrade prod-logs prod-ps prod-shell

prod-up:
	$(COMPOSE_PROD) up -d

prod-down:
	$(COMPOSE_PROD) down

prod-restart:
	$(COMPOSE_PROD) restart

prod-rebuild:
	$(COMPOSE_PROD) build --no-cache backend

prod-upgrade:
	git fetch origin develop && git reset --hard origin/develop

prod-logs:
	$(COMPOSE_PROD) logs -f $(BACKEND)

prod-ps:
	$(COMPOSE_PROD) ps

prod-shell:
	$(COMPOSE_PROD) exec $(BACKEND) /bin/sh


# --------------------
# PROD DATABASE
# --------------------
.PHONY: prod-migrate prod-makemigration prod-downgrade

prod-migrate:
	$(COMPOSE_PROD) exec -T $(BACKEND) alembic upgrade head

prod-makemigration:
	$(COMPOSE_PROD) exec -T $(BACKEND) alembic revision --autogenerate -m "$(name)"

prod-downgrade:
	$(COMPOSE_PROD) exec -T $(BACKEND) alembic downgrade -1


# --------------------
# PROD OPS (scripts)
# --------------------
.PHONY: prod-deploy prod-status prod-backup prod-clean

prod-deploy:
	./scripts/prod-deploy.sh

prod-status:
	./scripts/status-check.sh

prod-backup:
	./scripts/backup.sh all

prod-clean:
	$(COMPOSE_PROD) down -v