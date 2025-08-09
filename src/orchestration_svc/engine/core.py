
"""
Core orchestration engine logic.
Coordinates workflow execution only—no business logic, adapters, or integrations.
All data is handled as plain dicts with JSON-LD context.
"""


from typing import Optional, Any
from orchestration_svc.domain.ports import WorkflowRepositoryPort
from orchestration_svc.constants import JSONLD_CONTEXT


class OrchestrationEngine:

    def create_workflow(self, alias: str) -> dict[str, Any]:
        """
        Create a new workflow with a human-readable alias. Returns the created workflow dict.
        """
        if self.workflow_repo is None:
            raise RuntimeError("Workflow repository is not configured in OrchestrationEngine")
        return self.workflow_repo.create_workflow(alias)
    """
    The orchestration engine coordinates workflow execution.
    All adapters, integrations, and domain models are externalized.
    """

    def __init__(self, workflow_repo: WorkflowRepositoryPort) -> None:
        """
        Initialize the engine with a workflow repository
        (externalized, must implement WorkflowRepositoryPort).
        """
        self.workflow_repo = workflow_repo

    def start_workflow(self, workflow_id: str) -> Optional[dict[str, Any]]:
        """
        Start a workflow by opaque ID.
        Returns a plain dict (JSON-LD expected by API layer), or None if not found.
        Ensures @context is always attached using the shared constant.
        """
        if self.workflow_repo is None:
            raise RuntimeError(
                "Workflow repository is not configured in OrchestrationEngine"
            )
        workflow = self.workflow_repo.get_workflow(workflow_id)
        if workflow is not None:
            # Attach JSON-LD context if not already present
            if "@context" not in workflow:
                workflow["@context"] = JSONLD_CONTEXT
        return workflow
