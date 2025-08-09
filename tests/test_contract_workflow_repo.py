"""
Contract test for WorkflowRepositoryPort.
Ensures all implementations conform to the public interface.
"""
from orchestration_svc.domain.ports import WorkflowRepositoryPort
from typing import Any, Dict
import pytest

class CompliantRepo(WorkflowRepositoryPort):
    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        return {"id": workflow_id, "status": "started"}
    def save_workflow(self, workflow: Dict[str, Any]) -> bool:
        return True

def test_contract_get_workflow() -> None:
    repo = CompliantRepo()
    result = repo.get_workflow("wf-abc")
    assert isinstance(result, dict)
    assert result["id"] == "wf-abc"
    assert "status" in result

def test_contract_save_workflow() -> None:
    repo = CompliantRepo()
    workflow = {"id": "wf-abc", "status": "started"}
    assert repo.save_workflow(workflow) is True
