# API Documentation

## Overview
This service exposes only orchestration APIs and interfaces/ports. All business logic, persistence, and integrations are handled externally.

## OpenAPI/Swagger
- Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- OpenAPI schema: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

## Example Payloads
See the README for example request/response payloads.

## Error Handling
All errors use a shared, DRY schema:
```json
{
  "error": {
    "code": "WORKFLOW_NOT_FOUND",
    "message": "Workflow not found",
    "detail": "Extra error details (optional)"
  }
}
```

## Versioning
If you need to add new endpoints, consider versioning your API routes (e.g., `/v1/`).
