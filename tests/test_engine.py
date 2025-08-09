"""
Test suite for the orchestration engine.
All ports/interfaces are mocked for isolation and clarity.
Inspired by the highest standards of software craftsmanship.
"""
import pytest
import uuid
from orchestration_svc.engine.core import OrchestrationEngine
from typing import Any, Dict, Callable
from .utils import MockWorkflowRepo


# Edge-case: malformed workflow IDs
@pytest.mark.parametrize("workflow_id", [None, 123, 45.6, b"bytes", [], {}])
def test_start_workflow_malformed_id(workflow_id: str) -> None:
    """
    Test OrchestrationEngine.start_workflow returns None for malformed/non-string workflow IDs.
    """
    repo = MockWorkflowRepo(known_workflow_ids={"valid-id"})
    engine = OrchestrationEngine(workflow_repo=repo)
    result = engine.start_workflow(workflow_id)
    assert result is None


@pytest.mark.parametrize(
    "workflow_id,expected",
    [
        (
            str(uuid.uuid4()),
            lambda wid: {"id": wid, "alias": "Test Workflow", "status": "started"},
        ),
        (
            str(uuid.uuid4()),
            lambda wid: {"id": wid, "alias": "Test Workflow", "status": "started"},
        ),
    ],
)
def test_start_workflow_success(
    workflow_id: str, expected: Callable[[str], Dict[str, Any]]
) -> None:
    """
    Test OrchestrationEngine.start_workflow for all valid/edge-case workflow IDs.
    """
    repo = MockWorkflowRepo(known_workflow_ids={workflow_id})
    engine = OrchestrationEngine(workflow_repo=repo)
    result = engine.start_workflow(workflow_id)
    exp = expected(workflow_id)
    assert result is not None and result["id"] == exp["id"]
    assert result is not None and result["alias"] == exp["alias"]
    assert result is not None and result["status"] == exp["status"]
    assert result is not None and "@context" in result
    assert result is not None and result["@context"]["@vocab"] == "https://schema.org/"
    assert result is not None and result["@context"]["id"] == "@id"
    assert result is not None and result["@context"]["alias"] == "rdfs:label"
    assert result is not None and result["@context"]["status"] == "schema:status"


@pytest.mark.parametrize("workflow_id", [str(uuid.uuid4()), str(uuid.uuid4())])
def test_start_workflow_not_found(workflow_id: str) -> None:
    """
    Test OrchestrationEngine.start_workflow returns None for missing workflows.
    """
    repo = MockWorkflowRepo(known_workflow_ids=set())
    engine = OrchestrationEngine(workflow_repo=repo)
    result = engine.start_workflow(workflow_id)
    assert result is None


def test_start_workflow_engine_not_configured() -> None:
    """
    Test OrchestrationEngine raises RuntimeError if repo is None.
    """
    engine = OrchestrationEngine(workflow_repo=None)  # type: ignore[arg-type]
    with pytest.raises(RuntimeError):
        engine.start_workflow("wf-123")
