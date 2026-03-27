# TokenGuard (Link Tracking Service)

## Overview

TokenGuard — backend-сервис для создания, редиректа и трекинга ссылок с аналитикой и эксплуатационными инструментами.

Система ориентирована на self-hosted deployment через Docker и включает инфраструктурные инструменты для деплоя, миграций, бэкапов и мониторинга.

---

## Architecture

### Runtime components

* Backend API: FastAPI (Uvicorn)
* Database: PostgreSQL 16
* Static frontend: встроен в backend image
* Reverse proxy: внешний (Nginx / аналог), в compose не входит

---

## Deployment model

* Git-based deployment (branch: develop)
* Docker immutable image rebuild per release
* Full restart strategy (без rolling update)
* Post-deploy migrations
* Pre-deploy backup

---

## Project structure

backend / application backend
frontend / frontend build source
scripts / operational scripts (deploy, backup, status)
alembic / migrations
docker-compose.prod.yml / production stack
backend/Dockerfile.prod / multi-stage build
Makefile / operational entrypoints
constraints.txt / dependency specification

---

## Requirements

### System level

* Docker Engine 24+
* Docker Compose v2
* Git
* OpenSSL
* curl
* PostgreSQL client tools (inside container)

---

## Configuration

Environment variables (.env):

Required:

* POSTGRES_DB
* POSTGRES_USER
* POSTGRES_PASSWORD

Optional:

* REDIS_URL
* ENVIRONMENT

---

## Build process

Frontend is built during Docker image creation:

* Node.js 20 stage compiles frontend
* npm ci installs dependencies
* npm run build produces static assets
* Output is copied into backend static directory

Backend image:

* Python 3.10 slim
* System dependencies installed via apt
* Python dependencies installed via pip
* Non-root execution user (appuser)

---

## Deployment

Primary command:
make prod-deploy

Deployment pipeline:

1. Full backup (DB, code, metadata)
2. Git fetch + hard reset to origin/develop
3. Stop containers
4. Rebuild backend image
5. Start containers
6. Wait for health endpoint
7. Run database migrations
8. Status validation

---

## Makefile operations

Production:

* prod-up: start services
* prod-down: stop services
* prod-restart: restart services
* prod-rebuild: rebuild backend image
* prod-deploy: full deployment
* prod-migrate: run Alembic migrations
* prod-status: system diagnostics
* prod-backup: backup pipeline
* prod-clean: remove volumes

Development:

* dev-up / dev-down
* dev-logs
* dev-test
* dev-migrate

---

## Database migrations

Tooling: Alembic

Execution:

* runs inside backend container
* triggered after successful startup + health check

---

## Backup system

Features:

* PostgreSQL dump (compressed)
* Code snapshot archive
* Static files snapshot
* Update metadata (git state)
* Retention cleanup (30 days)
* Optional Google Drive upload via rclone

Execution:
triggered automatically before deployment

---

## Health & monitoring

Endpoints:

* /health (internal backend)
* [https://tokenguard.ru](https://tokenguard.ru) (external check)

Status tool:
make prod-status

Checks:

* Docker container state
* PostgreSQL readiness
* Nginx/systemd status
* SSL certificate validity
* System resources (CPU, RAM, disk)

---

## Docker Compose (production)

Services:

backend:

* FastAPI application
* Port 8000 exposed
* Depends on postgres
* Mounts alembic configuration

postgres:

* PostgreSQL 16 Alpine
* Persistent volume storage

---

## Deployment constraints

* Single-node architecture
* No horizontal scaling
* No rolling deployments
* No automatic rollback
* Git-based release mechanism

---

## Failure domains

Known risk areas:

* Git reset conflicts during deployment
* Migration timing vs service readiness
* Database startup race conditions
* Docker volume permission issues
* Healthcheck timeout edge cases

---

## Security model

* Secrets stored in environment variables
* No hardcoded credentials in repo
* DB accessible only within Docker network (except exposed port if enabled)
* No application-level auth assumed at infra layer

---

## Maintenance

Backup:
make prod-backup

Logs:
make prod-logs

Full cleanup:
make prod-clean

---

## Summary

TokenGuard is a single-node production deployment system designed for deterministic rebuilds, explicit operational scripts, and controlled Git-based release flow with minimal orchestration overhead.
