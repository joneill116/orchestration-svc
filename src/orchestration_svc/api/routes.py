
"""
API routes for orchestration-svc.
Exposes orchestration endpoints only—no business logic or integrations.
All dependencies are injected and mockable for microservice clarity.
"""

from fastapi import APIRouter, Depends

from orchestration_svc.engine.core import OrchestrationEngine
from orchestration_svc.domain.ports import WorkflowDict
from orchestration_svc.container import Container



router = APIRouter()


# Dependency: resolve engine from DI container at request time
def get_engine() -> OrchestrationEngine:
    return Container.engine()



@router.get(
    "/workflows/{workflow_id}",
    response_model=WorkflowDict,
    summary="Get workflow by ID",
    response_description="The workflow data as a dictionary",
    tags=["Workflows"],
)
def get_workflow(
    workflow_id: str,
    engine: OrchestrationEngine = Depends(get_engine),
) -> dict:
    """
    Retrieve a workflow by its opaque ID, with semantic annotations (JSON-LD).
    The returned object includes an 'id' (opaque, meaningless),
    an optional 'alias' (business-meaningful),
    and a JSON-LD @context for ontology alignment.
    ---
    - **workflow_id**: The workflow identifier (opaque)
        - description: Opaque workflow identifier (not business-meaningful)
        - x-ontology: @id
    - **alias**: Business-meaningful alias or label for the workflow
        - x-ontology: rdfs:label
    - **status**: Current status of the workflow
        - x-ontology: schema:status
    - **returns**: The workflow data as a WorkflowDict (with 'id', 'alias', etc.)
      and semantic annotations
    Supports both sync and async implementations.
    Logging and error handling should be consistent and
    observable.
    """
    workflow = engine.start_workflow(workflow_id)
    if workflow is None:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail="Workflow not found",
        )
    # Add JSON-LD @context for semantic clarity (example using schema.org and custom terms)
    jsonld_context = {
        "@vocab": "https://schema.org/",
        "id": "@id",
        "alias": "rdfs:label",
        "status": "schema:status",
    }
    # Compose JSON-LD response
    response = {
        "@context": jsonld_context,
        **workflow,
    }
    return response
