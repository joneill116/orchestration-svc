"""
API routes for orchestration-svc.
Exposes orchestration endpoints only—no business logic or integrations.
All dependencies are injected and mockable for microservice clarity.
"""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi import status

from orchestration_svc.engine.core import OrchestrationEngine


router = APIRouter()




# Dependency: resolve engine from the app's DI container at request time
from fastapi import Request
def get_engine(request: Request) -> OrchestrationEngine:
    return request.app.container.engine()

# Shared JSON-LD context for all workflow responses
JSONLD_CONTEXT = {
    "@vocab": "https://schema.org/",
    "id": "@id",
    "alias": "rdfs:label",
    "status": "schema:status",
}

ERROR_SCHEMA = {
    "type": "object",
    "properties": {
        "error": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "example": "WORKFLOW_NOT_FOUND"},
                "message": {"type": "string", "example": "Workflow not found"},
                "detail": {"type": "string", "example": "Extra error details (optional)"},
            },
            "required": ["code", "message"]
        }
    },
    "required": ["error"]
}

@router.get(
    "/workflows/{workflow_id}",
    summary="Get workflow by ID",
    response_description="The workflow data as a JSON-LD dictionary",
    tags=["Workflows"],
    responses={
        404: {"description": "Not found", "content": {"application/json": {"schema": ERROR_SCHEMA}}},
        500: {"description": "Internal error", "content": {"application/json": {"schema": ERROR_SCHEMA}}},
    }
)
def get_workflow(workflow_id: str, engine: OrchestrationEngine = Depends(get_engine)) -> dict:
    """
    Retrieve a workflow by its opaque ID, returning a JSON-LD dictionary.
    The response includes:
      - 'id': Opaque workflow identifier (@id)
      - 'alias': Optional business-meaningful label (rdfs:label)
      - 'status': Current workflow status (schema:status)
      - '@context': JSON-LD context for semantic clarity
    All business logic and integrations are externalized.
    """
    try:
        workflow = engine.start_workflow(workflow_id)
    except RuntimeError as e:
        # Use new error model
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "ENGINE_ERROR",
                    "message": "Engine failure",
                    "detail": str(e),
                }
            },
        )
    if workflow is None:
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "code": "WORKFLOW_NOT_FOUND",
                    "message": "Workflow not found",
                }
            },
        )
    response = dict(workflow)
    response["@context"] = JSONLD_CONTEXT
    return response
