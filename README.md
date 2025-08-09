# orchestration-svc

<p align="center">
  <img alt="Build Status" src="https://img.shields.io/github/actions/workflow/status/joneill116/orchestration-svc/ci.yml?branch=dev">
  <img alt="Coverage" src="https://img.shields.io/codecov/c/github/joneill116/orchestration-svc/dev">
  <img alt="License" src="https://img.shields.io/github/license/joneill116/orchestration-svc">
  <img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/fastapi">
</p>

<p align="center">
  <b>Minimal, world-class orchestration service core</b><br>
  <i>Only orchestration logic, API, and interfaces/ports. All business logic, adapters, and domain models are externalized.</i>
</p>

---

<details>
<summary><b>Architecture Diagram</b> (click to expand)</summary>

See <a href="./ARCHITECTURE.md">ARCHITECTURE.md</a> for a high-level diagram and explanation.

</details>

---

## Table of Contents

- [Philosophy](#philosophy)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Quickstart](#quickstart)
- [API Example Payloads](#api-example-payloads)
- [Production & Security Notes](#production--security-notes)
- [Versioning Policy](#versioning-policy)
- [Project Resources](#project-resources)
- [FAQ](#faq)


## Philosophy
- **Single Responsibility:** Only orchestration logic, API, and interfaces/ports live here.
- **Microservice-First:** No adapters, integrations, or domain models—these are externalized and versioned.
- **Testability:** All ports/interfaces are mockable; the suite is fully tested.
- **Clarity:** Structure and naming are intention-revealing.



## Architecture
- **Boundaries:** This service exposes only orchestration APIs and interfaces/ports. All business logic, persistence, integrations, and cross-cutting concerns are handled by other microservices or libraries.
- **Contracts:** All interfaces/ports are public, versioned contracts. API is documented and ready for client generation.
- **Extensibility:** New adapters, integrations, or workflow steps are added by implementing ports in external services.

For a visual overview, see the <a href="./ARCHITECTURE.md">architecture diagram</a>.

## Project Structure
```
.
├── src/
│   └── orchestration_svc/
│       ├── api/
│       │   └── routes.py
│       ├── engine/
│       │   └── core.py
│       ├── domain/
│       │   └── ports.py
│       ├── container.py
│       ├── config.py
│       └── main.py
├── tests/
│   ├── test_engine.py
│   └── test_api.py
├── pyproject.toml
├── Makefile
├── .gitignore
└── README.md
```

---
### Run the service
```sh
poetry run uvicorn src.orchestration_svc.main:app --reload
```

### Run tests
```sh
poetry run pytest
```



## Quickstart

### Requirements
- Python 3.9–3.12+
- [Poetry](https://python-poetry.org/)

### Install dependencies
```sh
poetry install
```

### Run the service
```sh
poetry run uvicorn src.orchestration_svc.main:app --reload
```

### Run tests
```sh
poetry run pytest
```

### Run tests with coverage
```sh
poetry run pytest --cov=src/orchestration_svc --cov=tests --cov-report=term-missing
```

### Type checking
```sh
poetry run mypy src/orchestration_svc/ tests/
```

### Linting
```sh
poetry run ruff check .
```


### API documentation (OpenAPI/Swagger)
- Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs) *(run the service locally first)*
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc) *(run the service locally first)*


---

## API Example Payloads

### Example: Create Workflow (Request)
```json
{
  "alias": "Test Workflow"
}
```

### Example: Workflow (Success Response)
```json
{
  "id": "b7e6c2e2-2c3a-4e7a-8e2a-1b2c3d4e5f6a",
  "alias": "Test Workflow",
  "status": "started",
  "@context": {
    "@vocab": "https://schema.org/",
    "id": "@id",
    "alias": "rdfs:label",
    "status": "schema:status"
  }
}
```

### Example: Error Response (404 Not Found)
```json
{
  "error": {
    "code": "WORKFLOW_NOT_FOUND",
    "message": "Workflow not found"
  }
}
```

### Example: Error Response (500 Engine Error)
```json
{
  "error": {
    "code": "ENGINE_ERROR",
    "message": "Engine failure",
    "detail": "Workflow repository is not configured in OrchestrationEngine"
  }
}
```

---

## Production & Security Notes

- **CORS:** By default, CORS is open to all origins for development. Restrict `allow_origins` in production.
- **Secrets:** Never commit secrets. Use environment variables or a vault.
- **Auth:** Add OIDC/JWT middleware and RBAC as needed for your environment.
- **SBOM & Supply Chain:** Generate a Software Bill of Materials (SBOM) and sign builds for supply chain security.
- **Liveness/Readiness:** Add endpoints and document for K8s if deploying to production.

---

## Versioning Policy

This project follows [Semantic Versioning](https://semver.org/). Breaking changes are documented in the [CHANGELOG.md](./CHANGELOG.md) and communicated via release notes.

---

## Project Resources

- [Architecture Diagram](./ARCHITECTURE.md)
- [Changelog](./CHANGELOG.md)
- [Contributing Guide](./CONTRIBUTING.md)
- [Code of Conduct](./CODE_OF_CONDUCT)
- [Security Policy](./SECURITY.md)
- [Code Owners](./CODEOWNERS)
- [Runbook](./RUNBOOK.md)

---

## FAQ

**Q: How do I add a new adapter or integration?**
A: Implement the relevant port/interface in your own service or library. This repo only defines contracts and orchestration logic.

**Q: How do I run the service in production?**
A: Use a production-grade ASGI server (e.g., uvicorn or gunicorn), restrict CORS, and add authentication middleware as needed.

**Q: Where do I find the API schema?**
A: Visit `/docs` or `/redoc` when running locally, or see the OpenAPI spec at `/openapi.json`.

**Q: How do I get support or report a security issue?**
A: See [SECURITY.md](./SECURITY.md) for the disclosure process, or open an issue for general support.

---

## Architecture
- **src/orchestration_svc/api/routes.py**: API endpoints, orchestration only.
- **src/orchestration_svc/engine/core.py**: Orchestration logic, no business logic.
- **src/orchestration_svc/container.py**: Dependency injection container.
