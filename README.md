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
```sh
poetry run pytest
```

## API

- `GET /api/workflows/{workflow_id}`: Retrieve workflow by ID (opaque, not business-meaningful)
    - Returns: Workflow object with semantic JSON-LD annotations and OpenAPI/x-ontology field docs.
    - Returns 404 if not found (no `@context` in error response).
    - Supports both sync and async implementations.
    - Logging and error handling are consistent and observable.

### API Response Contract (JSON-LD)
```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "id": "@id",
    "alias": "rdfs:label",
    "status": "schema:status"
  },
  "id": "wf-456",
  "alias": "Order Processing",
  "status": "started"
}
```

#### Field Semantics (OpenAPI/x-ontology)
- `id`: Opaque workflow identifier (not business-meaningful). `x-ontology: @id`
- `alias`: Business-meaningful alias or label. `x-ontology: rdfs:label`
- `status`: Current status of the workflow. `x-ontology: schema:status`

#### Error Handling
- 404: Workflow not found (no `@context` in error response)

#### Semantic/Ontological Alignment
- All API responses are JSON-LD with a semantic `@context` for knowledge graph and ontology integration.
- All fields are documented with OpenAPI `description` and `x-ontology` annotations.

#### Async/Sync
- All interfaces and implementations support both sync and async patterns.

#### Logging & Observability
- All errors and key events must be logged with correlation IDs for traceability.

## Extending & Integrating
- Implement ports in `domain/ports.py` in your own adapters/services.
- Wire them up in `container.py` using dependency-injector.
- All integrations are via public, versioned contracts—never direct imports.
- This service is stateless and horizontally scalable.

## Microservice Integration
- This service is designed to be deployed independently and communicate with other services via APIs or events.
- All state, persistence, and business logic are externalized.
- See `domain/ports.py` for contract definitions.

---

> Designed for clarity, modularity, and testability by inspiration from Fowler, Beck, Evans, and the world’s best architects.
