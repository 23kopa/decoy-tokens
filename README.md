# 🔐 TokenGuard

> Self-hosted decoy token platform for tracking link and email interactions, collecting request intelligence, and reviewing token-triggered events.

![Python](https://img.shields.io/badge/python-3.10-blue)
![FastAPI](https://img.shields.io/badge/framework-FastAPI-009688)
![PostgreSQL](https://img.shields.io/badge/database-PostgreSQL%2016-336791)
![Docker](https://img.shields.io/badge/docker-ready-2496ED)
![Alembic](https://img.shields.io/badge/migrations-Alembic-darkred)
![Vite](https://img.shields.io/badge/frontend-Vite-646CFF)

---

## 📚 Table of Contents

* [Overview](#-overview)
* [Features](#-features)
* [Architecture](#-architecture)
* [Project Structure](#-project-structure)
* [Tech Stack](#-tech-stack)
* [Configuration](#-configuration)
* [Run Locally](#-run-locally)
* [Production Deployment](#-production-deployment)
* [Makefile Commands](#-makefile-commands)
* [Database Migrations](#-database-migrations)
* [How Token Tracking Works](#-how-token-tracking-works)
* [Frontend](#-frontend)
* [Operational Scripts](#-operational-scripts)
* [Security Notes](#-security-notes)
* [Known Constraints](#-known-constraints)

---

## 🚀 Overview

**TokenGuard** is a self-hosted service for creating and managing **decoy tokens** that record access events and expose operational analytics.

It is built around a FastAPI backend, PostgreSQL storage, server-rendered templates, and a Vite-based frontend pipeline. The system supports token creation, token activation via public trigger routes, request metadata collection, event logging, deduplication, IP and geo analysis, and dashboard-based event review.

---

## ✨ Features

* Create and manage **decoy tokens**
* Support for multiple token types:

  * **link**
  * **email**
* Public trigger endpoints for token activation
* Request intelligence collection:

  * IP detection
  * proxy-aware extraction
  * header parsing
  * browser query hints
  * port capture
* Geo/IP enrichment via **GeoLite2**
* Fingerprint generation and deduplication
* Bot detection from request metadata
* Event history and token statistics
* API routes and server-rendered dashboard pages
* Docker-based local and production environments
* Alembic migrations
* Backup / deploy / status scripts

---

## 🏗 Architecture

The project follows a layered backend structure with clear separation of concerns.

### Backend layers

* **Domain**
  Core entities and value objects:

  * `Token`
  * `TokenEvent`
  * `User`

* **Application**
  Use cases and repository ports:

  * token creation and activation
  * authentication and registration
  * event retrieval and logging
  * token statistics

* **Infrastructure**
  Concrete implementations for:

  * database models and repositories
  * security helpers
  * request collection
  * logging and utility services

* **Web**
  FastAPI routes, dependencies, middlewares, presenters, and security integration

### Runtime flow

1. A user creates a token
2. A public trigger URL is generated
3. Someone activates the token
4. The backend collects request metadata
5. The system enriches the event with IP, geo, and header data
6. A fingerprint is generated
7. Duplicates and bots are evaluated
8. The event is stored and exposed in the dashboard and API

---

## 📁 Project Structure

```
decoy-tokens
├─ backend/
│  ├─ app/
│  │  ├─ application/      # Use cases, ports, application errors
│  │  ├─ domain/           # Entities and value objects
│  │  ├─ infrastructure/   # DB, repositories, security, HTTP collectors, utils
│  │  ├─ services/         # Decoy token engines and analysis utilities
│  │  ├─ web/              # Routes, middlewares, presenters, dependencies
│  │  ├─ templates/        # Jinja templates
│  │  ├─ static/           # Built frontend assets
│  │  ├─ data/             # GeoIP databases, media assets
│  │  └─ main.py           # FastAPI entrypoint
│  ├─ alembic/             # Migration environment and versions
│  ├─ Dockerfile
│  └─ Dockerfile.prod
├─ frontend/               # Vite frontend source
├─ deploy/nginx/           # Nginx config
├─ scripts/                # Deploy, backup, frontend prep, status scripts
├─ docker-compose.yml      # Development stack
├─ docker-compose.prod.yml # Production stack
├─ alembic.ini
├─ Makefile
├─ requirements.txt
└─ uv.lock
```

---

## 🧰 Tech Stack

### Backend

* Python 3.10
* FastAPI
* Uvicorn
* PostgreSQL 16
* Alembic

### Frontend

* Vite
* Vanilla JavaScript modules
* CSS build pipeline with static asset output into the backend

### Infrastructure

* Docker / Docker Compose
* Nginx
* GeoLite2 databases for IP enrichment
* `uv` for dependency installation in container builds

---

## ⚙️ Configuration

Create a `.env` file:

```
APP_ENV=dev
SESSION_SECRET_KEY=

PUBLIC_BASE_URL=http://localhost:8000

DATABASE_URL=
POSTGRES_USER=
POSTGRES_PASSWORD=

RECAPTCHA_SITE_KEY=
RECAPTCHA_SECRET_KEY=
```

### Main environment variables

| Variable               | Description                                          |
| ---------------------- | ---------------------------------------------------- |
| `APP_ENV`              | Application environment (`dev` / `prod`)             |
| `SESSION_SECRET_KEY`   | Secret used for session security                     |
| `PUBLIC_BASE_URL`      | Public base URL used to generate token trigger links |
| `DATABASE_URL`         | Database connection string                           |
| `POSTGRES_USER`        | PostgreSQL user                                      |
| `POSTGRES_PASSWORD`    | PostgreSQL password                                  |
| `RECAPTCHA_SITE_KEY`   | Public reCAPTCHA key                                 |
| `RECAPTCHA_SECRET_KEY` | Private reCAPTCHA secret                             |

---

## 🧪 Run Locally

### With Docker Compose

Start development services:

```
make dev-up
```

Stop them:

```
make dev-down
```

Open a backend shell:

```
make dev-shell
```

View backend logs:

```
make dev-logs
```

### Frontend development

Install frontend dependencies:

```
make dev-front-install
```

Run the Vite dev server:

```
make dev-front
```

Build frontend assets:

```
make dev-front-build
```

---

## 🚀 Production Deployment

Production services are defined in `docker-compose.prod.yml`.

### Main services

* **backend**

  * built from `backend/Dockerfile.prod`
  * runs `uvicorn backend.app.main:app`
  * exposes port `8000`
  * loads environment from `.env`

* **postgres**

  * uses `postgres:16-alpine`
  * stores persistent data in a Docker volume
  * exposes port `5432`

### Deploy command

```
make prod-deploy
```

### Production operations

```
make prod-up
make prod-down
make prod-restart
make prod-logs
make prod-ps
make prod-shell
```

---

## 🛠 Makefile Commands

### Development

```
make dev-up
make dev-build
make dev-down
make dev-restart
make dev-logs
make dev-ps
make dev-shell

make dev-migrate
make dev-makemigration name="message"
make dev-downgrade

make dev-front
make dev-front-build
make dev-front-install

make dev-test
```

### Production

```
make prod-up
make prod-down
make prod-restart
make prod-rebuild
make prod-upgrade
make prod-logs
make prod-ps
make prod-shell

make prod-migrate
make prod-makemigration name="message"
make prod-downgrade

make prod-deploy
make prod-deploy-clean
make prod-status
make prod-backup
make prod-clean
```

---

## 🧬 Database Migrations

Migrations are managed with **Alembic**.

Existing migration history includes:

* initial schema setup
* token slug support and backfill
* removal of token secret hash

Run migrations in development:

```
make dev-migrate
```

Run migrations in production:

```
make prod-migrate
```

Create a new migration:

```
make dev-makemigration name="add_new_field"
```

---

## 🕵️ How Token Tracking Works

Token tracking is centered around the token activation flow.

### Token creation

The token creation use case:

* validates token input
* supports `link` and `email` token types
* generates a unique slug
* builds a public trigger URL using `PUBLIC_BASE_URL`
* stores the token as active by default

### Token activation

When a token is activated:

* the system resolves the token by slug
* ensures the token exists and is active
* logs an event for the request

### Request collection

The request collector gathers:

* detected client IP
* proxy-aware IP metadata
* geo information
* request headers
* HTTP method
* request path
* selected browser/client query hints
* client port
* IP version

### Event logging

The event logger then:

* builds a request fingerprint
* checks duplicates through a deduplication strategy
* inspects user agent data for bot detection
* stores event metadata including:

  * IP history
  * headers
  * geo data
  * ASN / organization
  * bot info
  * timestamps

This makes TokenGuard suitable for controlled tracking, interaction visibility, and event review workflows.

---

## 🖥 Frontend

The frontend source lives in `frontend/` and is organized by feature modules:

* `events`
* `tokens`
* `shared`

Built assets are served by the backend through:

* `backend/app/static`
* `backend/app/templates`

The UI includes:

* token creation flows
* dashboard pages
* token event modals
* reusable template components and macros

---

## 📜 Operational Scripts

The `scripts/` directory contains operational helpers:

* `prod-deploy.sh` — production deployment flow
* `backup.sh` — backup workflow
* `auto-backup.sh` — automated backup execution
* `prepare-front.sh` — frontend preparation/build support
* `status-check.sh` — service and environment checks

Useful commands:

```
make prod-deploy
make prod-backup
make prod-status
```

---

## 🔐 Security Notes

* Session handling is configured via `SESSION_SECRET_KEY`
* reCAPTCHA keys are supported for public-facing protection
* Password and token-related security helpers live in the infrastructure and web security layers
* Proxy/IP handling is explicitly implemented for better request attribution
* Sensitive values should be provided only through environment variables

---

## ⚠️ Known Constraints

* Single PostgreSQL instance
* Docker Compose based deployment model
* No built-in horizontal scaling
* No rolling deployment strategy in the current setup
* Public token trigger endpoints require correct reverse proxy and HTTPS configuration
* GeoIP accuracy depends on local GeoLite2 database freshness

---

## 🧾 Summary

TokenGuard is a self-hosted decoy token platform built around:

* clean backend layering
* structured event collection
* link and email token workflows
* Docker-based operations
* dashboard and API access to trigger analytics

It is designed for teams that want a lightweight, inspectable, and extensible token tracking system without heavy orchestration.
