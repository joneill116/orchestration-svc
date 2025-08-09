import pytest

# Edge-case: malformed workflow IDs
@pytest.mark.parametrize("workflow_id", [None, 123, 45.6, b"bytes", [], {}])
def test_start_workflow_malformed_id(workflow_id):
    """
    Test OrchestrationEngine.start_workflow returns None for malformed/non-string workflow IDs.
    """
    repo = MockWorkflowRepo(known_workflow_ids={"valid-id"})
    engine = OrchestrationEngine(workflow_repo=repo)
    result = engine.start_workflow(workflow_id)
    assert result is None

"""
Test suite for the orchestration engine.
All ports/interfaces are mocked for isolation and clarity.
Inspired by the highest standards of software craftsmanship.
"""

from orchestration_svc.engine.core import OrchestrationEngine

from .utils import MockWorkflowRepo
import uuid


import pytest

@pytest.mark.parametrize(
    "workflow_id,expected",
    [
        (str(uuid.uuid4()), lambda wid: {"id": wid, "alias": "Test Workflow", "status": "started"}),
        (str(uuid.uuid4()), lambda wid: {"id": wid, "alias": "Test Workflow", "status": "started"}),
    ]
)
def test_start_workflow_success(workflow_id, expected):
    """
    Test OrchestrationEngine.start_workflow for all valid/edge-case workflow IDs.
    """
    repo = MockWorkflowRepo(known_workflow_ids={workflow_id})
    engine = OrchestrationEngine(workflow_repo=repo)
    result = engine.start_workflow(workflow_id)
    exp = expected(workflow_id)
    assert result["id"] == exp["id"]
    assert result["alias"] == exp["alias"]
    assert result["status"] == exp["status"]
    assert "@context" in result
    assert result["@context"]["@vocab"] == "https://schema.org/"
    assert result["@context"]["id"] == "@id"
    assert result["@context"]["alias"] == "rdfs:label"
    assert result["@context"]["status"] == "schema:status"

@pytest.mark.parametrize("workflow_id", [str(uuid.uuid4()), str(uuid.uuid4())])
def test_start_workflow_not_found(workflow_id):
    """
    Test OrchestrationEngine.start_workflow returns None for missing workflows.
    """
    repo = MockWorkflowRepo(known_workflow_ids=set())
    engine = OrchestrationEngine(workflow_repo=repo)
    result = engine.start_workflow(workflow_id)
    assert result is None

def test_start_workflow_engine_not_configured():
    """
    Test OrchestrationEngine raises RuntimeError if repo is None.
    """
    engine = OrchestrationEngine(workflow_repo=None)
    with pytest.raises(RuntimeError):
        engine.start_workflow("wf-123")
