
"""
Test suite for the orchestration engine.
All ports/interfaces are mocked for isolation and clarity.
Inspired by the highest standards of software craftsmanship.
"""

from orchestration_svc.engine.core import OrchestrationEngine
from orchestration_svc.domain.ports import WorkflowRepositoryPort
import pytest
from typing import Any, Dict

class DummyWorkflowRepo(WorkflowRepositoryPort):
    """A mock implementation of WorkflowRepositoryPort for testing."""
    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Return a dummy workflow dict."""
        return {"id": workflow_id, "status": "started"}

    def save_workflow(self, workflow: Dict[str, Any]) -> bool:
        """Pretend to save a workflow and return True."""
        return True

def test_start_workflow() -> None:
    """
    Test that OrchestrationEngine.start_workflow returns the correct workflow dict.
    Ensures the engine interacts with the port as expected.
    """
    repo = DummyWorkflowRepo()
    engine = OrchestrationEngine(workflow_repo=repo)
    result = engine.start_workflow("wf-123")
    assert result["id"] == "wf-123"
    assert result["status"] == "started"
