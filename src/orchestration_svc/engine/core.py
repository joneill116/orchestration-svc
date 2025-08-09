
"""
Core orchestration engine logic.
Coordinates workflow execution only—no business logic, adapters, or integrations.
All data is handled as plain dicts with JSON-LD context.
"""


from typing import Optional
from orchestration_svc.domain.ports import WorkflowRepositoryPort

class OrchestrationEngine:
    """
    The orchestration engine coordinates workflow execution.
    All adapters, integrations, and domain models are externalized.
    """
    def __init__(self, workflow_repo: WorkflowRepositoryPort) -> None:
        """
        Initialize the engine with a workflow repository (externalized, must implement WorkflowRepositoryPort).
        """
        self.workflow_repo = workflow_repo

    def start_workflow(self, workflow_id: str) -> Optional[dict]:
        """
        Start a workflow by opaque ID.
        Returns a plain dict (JSON-LD expected by API layer), or None if not found.
        """
        if self.workflow_repo is None:
            raise RuntimeError(
                "Workflow repository is not configured in OrchestrationEngine"
            )
        workflow = self.workflow_repo.get_workflow(workflow_id)
        # ... orchestrate workflow ...
        return workflow
