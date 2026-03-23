# Decoy Tokens

Decoy Tokens is an open-source security solution designed to detect unauthorized access, lateral movement, and early-stage intrusion attempts within your systems or network. It allows you to generate a variety of "decoy" artifacts—tokens—that act as early warning traps. Any interaction with such a token triggers an alert and provides visibility into potential compromise long before real damage occurs.

This project provides a free online service for generating, distributing, and monitoring decoy tokens across files, applications, infrastructure, and internal environments.

---

## Overview

A decoy token is a specially crafted artifact that appears legitimate and attractive to an attacker: a document, a link, a DNS record, a configuration file, or an executable. Once deployed into your environment, it behaves like a silent tripwire.

When an attacker opens, loads, or interacts with the token, the service instantly captures the event and reports it. Alerts include metadata such as:

* IP address
* Timestamp
* User agent or OS indicators
* Interaction type (HTTP access, DNS lookup, file opening, etc.)
* Token category and origin

This provides early detection in scenarios such as:

* Unauthorized access to files or endpoints
* Credential harvesting
* Lateral movement inside corporate networks
* Insider threat activity
* Cloud or server compromise

Decoy Tokens helps transform your system into a distributed honeypot network, where every planted artifact is a potential intrusion signal.

---

## Features

### Core Security Capabilities

* Generation of multiple token types (documents, URLs, DNS records, API keys, executables, configuration files).
* Real-time monitoring of token interactions.
* Immediate notifications via email or other channels.
* Metadata collection for each event.
* Designed to detect early signs of unauthorized access or reconnaissance.

### Backend Architecture

* FastAPI application server
* Asynchronous SQLAlchemy 2.0 with PostgreSQL
* Redis for caching, rate limiting, token metadata, and event buffering
* Alembic for migrations
* Modular domain-driven architecture (DDD principles)
* Session-based and token-based authentication

### Frontend & UI

* Jinja2 templates (server-side rendering)
* HTMX for dynamic and partial updates
* Alpine.js for lightweight interactivity
* Tailwind CSS for clean and efficient UI components

---

## Technology Stack

**Backend:**

* Python 3.x
* FastAPI
* SQLAlchemy 2.0 (async)
* PostgreSQL
* Redis
* Alembic
* Pydantic

**Frontend:**

* Jinja2 Templates
* HTMX
* Alpine.js
* Tailwind CSS

**Infrastructure:**

* Docker & Docker Compose
* Nginx (optional)
* Makefile-based automation

---

## Project Structure

The project follows a clean application architecture with distinct layers:

```
backend/app/
├── api/              # REST API routes, dependencies, schemas
├── web/              # Web UI routes, template rendering, htmx endpoints
├── templates/        # Jinja2 templates (pages, components, macros)
├── static/           # CSS, JS, images
├── core/             # App config, logging, security, i18n
├── domain/           # DDD domain entities and value objects
├── services/         # Application services and business logic
├── infrastructure/   # DB models, repositories, uow, redis, external providers
```

Additionally:
* `frontend/` contains Tailwind + JS tooling for local development.
* `docker-compose.*.yml` files manage the full environment.
* `scripts/` contains utility scripts for building, running, and migrating.

---

## Installation

Clone the repository:

```
git clone [https://github.com/23kopa/decoyTokens.git](https://github.com/23kopa/decoyTokens.git)
cd decoyTokens
```
Copy and configure environment variables:

```
cp .env.example .env
```

Start the development environment:

```
docker compose up --build
```

This launches:

* FastAPI backend
* PostgreSQL
* Redis
* Frontend builder (Tailwind)
* Auxiliary containers (if configured)

---

## Development

Use the `develop` branch for ongoing work:

```
git checkout develop
```

Create feature branches for tasks:

```
git checkout -b feature/<name>
```

Run tests (if enabled):

```
pytest
```

Apply database migrations:

```
scripts/migrate.sh
```

---

## Security Notes

Decoy Tokens should not replace traditional security measures, but extend them by providing:

* Behavioral intrusion detection
* Visibility into unauthorized file access
* Early compromise indicators
* Detection of attackers during reconnaissance phases

Use tokens sparingly and place them intentionally. Avoid exposing sensitive real data.

---

## Roadmap

* Additional token types (cloud credentials, SSH keys, config traps)
* Webhook integration for alerting
* Extended analytics dashboard
* Threat timeline view
* Open-source agent for automated deployment of tokens

---

## License

This project is distributed under the MIT License. See `LICENSE` for details.