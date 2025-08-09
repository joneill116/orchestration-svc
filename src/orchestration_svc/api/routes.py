"""
API routes for orchestration-svc.
Exposes orchestration endpoints only—no business logic or integrations.
All dependencies are injected and mockable for microservice clarity.
"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from orchestration_svc.engine.core import OrchestrationEngine
from orchestration_svc.constants import get_error_schema


router = APIRouter()


def get_engine(request: Request) -> OrchestrationEngine:
    return request.app.container.engine()  # type: ignore[no-any-return]


@router.get(
    "/workflows/{workflow_id}",
    summary="Get workflow by ID",
    response_description="The workflow data as a JSON-LD dictionary",
    tags=["Workflows"],
    responses={
        404: {
            "description": "Not found",
            "content": {"application/json": {"schema": get_error_schema()}},
        },
        500: {
            "description": "Internal error",
            "content": {"application/json": {"schema": get_error_schema()}},
        },
    },
)
def get_workflow(
    workflow_id: str,
    engine: OrchestrationEngine = Depends(get_engine),
) -> JSONResponse:
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
        error_schema = get_error_schema()
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "ENGINE_ERROR",
                    "message": "Engine failure",
                    "detail": str(e),
                    "_schema": error_schema["properties"]["error"],
                }
            },
        )
    if workflow is None:
        error_schema = get_error_schema()
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "code": "WORKFLOW_NOT_FOUND",
                    "message": "Workflow not found",
                    "_schema": error_schema["properties"]["error"],
                }
            },
        )
    return JSONResponse(content=workflow)
