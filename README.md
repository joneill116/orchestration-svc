# orchestration-svc

A minimal, world-class orchestration service core.

## Philosophy
- **Single Responsibility:** Only orchestration logic, API, and interfaces/ports live here.
- **Microservice-First:** No adapters, integrations, or domain models—these are externalized and versioned.
- **Testability:** All ports/interfaces are mockable; the suite is fully tested.
- **Clarity:** Structure and naming are intention-revealing.

## Architecture
- **Boundaries:** This service exposes only orchestration APIs and interfaces/ports. All business logic, persistence, integrations, and cross-cutting concerns are handled by other microservices or libraries.
- **Contracts:** All interfaces/ports are public, versioned contracts. API is documented and ready for client generation.
- **Extensibility:** New adapters, integrations, or workflow steps are added by implementing ports in external services.

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

## Quickstart
```sh
poetry install
poetry run uvicorn orchestration_svc.main:app --reload
```

## Testing

# orchestration-svc

A minimal, world-class orchestration service focused on modularity, testability, and clarity. All business logic, adapters, and domain models are externalized for maximum flexibility and maintainability.

---

## Features
- **Pure orchestration logic**: No business logic or integrations in the core service.
- **Semantic API**: JSON-LD responses for interoperability and clarity.
- **Dependency Injection**: All dependencies are injected and mockable for testability.
- **100% Test Coverage**: Comprehensive, parameterized, and reusable test suite.
- **Clean Architecture**: Ports/adapters pattern, clear separation of concerns.

---

## Quickstart

### Requirements
- Python 3.9+
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

---

## API Example

**Get Workflow by ID**

```
GET /api/v1/workflows/{workflow_id}
```

**Response (200):**
```json
{
  "id": "wf-123",
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

---

## Architecture
- **src/orchestration_svc/api/routes.py**: API endpoints, orchestration only.
- **src/orchestration_svc/engine/core.py**: Orchestration logic, no business logic.
- **src/orchestration_svc/container.py**: Dependency injection container.
- **tests/**: Comprehensive, reusable, and parameterized test suite.

---

## Contributing
See `CONTRIBUTING.md` for guidelines. All contributions must include tests and documentation.

---

## License
MIT
