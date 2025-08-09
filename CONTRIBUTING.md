# Contributing to orchestration-svc

Thank you for your interest in contributing! This service is designed for clarity, modularity, and microservice excellence.

## Guidelines
- All code must be type-annotated and documented.
- No adapters, integrations, or domain logic—only orchestration logic, API, and interfaces/ports.
- All ports/interfaces must be mockable and tested.
- PRs must pass CI (tests and linting).
- Follow the microservice-first philosophy: all integrations are external.

## Development
- Install dependencies: `poetry install`
- Run tests: `poetry run pytest`
- Lint: `flake8 src/`

## Extending
- Add new ports/interfaces in `domain/ports.py`.
- Do not add business logic or adapters here—create a new service/repo.

---

Inspired by the best practices of Fowler, Beck, Evans, and the world’s top engineers.
