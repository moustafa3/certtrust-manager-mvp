# CertTrust Manager MVP

CertTrust Manager MVP is a backend API built with Python and FastAPI.

The goal of this project is to simulate a simple certificate lifecycle management system.

## Project goal

This API allows teams to:

- register existing certificates
- track expiration dates
- detect certificates that will expire soon
- simulate certificate renewal
- revoke certificates
- keep audit logs for sensitive actions

## MVP scope

The MVP includes:

- health check endpoint
- certificate inventory
- certificate expiration tracking
- simulated renewal
- certificate revocation
- audit logs
- simple API key protection
- clean error handling
- tests
- Docker-based local environment
- CI pipeline with GitHub Actions

## Out of scope for MVP

The MVP does not include:

- real certificate generation
- real PKI
- OpenSSL integration
- real Certificate Authority
- Vault
- HSM
- Kubernetes
- automatic TLS discovery
- email notifications
- advanced RBAC

These topics may be added later in a future roadmap.

## Main modules

The project will be organized progressively around:

- API routes
- services
- repositories
- database models
- Pydantic schemas
- configuration
- security
- audit logs
- tests
- DevOps tooling

## Technical stack

- Python 3.12+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Pytest
- Docker
- Docker Compose
- GitHub Actions
- Ruff

## Git strategy

The project uses:

- `main` for stable code
- `develop` for active development
- `feature/*` branches for each feature

Commit messages follow Conventional Commits.

Examples:

- `docs: initialize project documentation`
- `chore: initialize FastAPI project`
- `feat: add health check endpoint`
- `test: add health check tests`
- `ci: add backend pipeline`

## Project vision

CertTrust Manager MVP is a simple but professional backend project focused on certificate lifecycle visibility, secure API design and traceability.

The goal is not to build a full PKI system.

The goal is to demonstrate clean backend architecture, business rules, testing, documentation and DevOps practices.