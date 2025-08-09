

# Standard library
from typing import Optional

# Third-party
import pytest
from fastapi.testclient import TestClient

# Local imports
from orchestration_svc.engine.core import OrchestrationEngine
from orchestration_svc.main import app
from orchestration_svc.domain.ports import WorkflowDict


# Shared dummy repo for all tests

class DummyWorkflowRepo:
    def get_workflow(self, workflow_id) -> Optional[WorkflowDict]:
        aliases = {
            "wf-456": "Order Processing",
            "wf-!@#": "Special Workflow",
            "": "Empty ID",
            "wf-über": "Unicode Workflow",
        }
        # For not-found and error tests, return None or raise as needed
        if workflow_id in ("does-not-exist", "wf-404", "nonexistent"):
            return None
        return WorkflowDict(id=workflow_id, alias=aliases.get(workflow_id, "Unknown"), status="started")



@pytest.fixture(autouse=True)
def reset_container():
    """Reset DI container overrides after each test for isolation."""
    yield
    app.container.engine.reset_last_overriding()



@pytest.mark.parametrize(
    "workflow_id,expected_status,expected_body",
    [
        ("wf-456", 200, {"id": "wf-456", "alias": "Order Processing", "status": "started"}),
        ("wf-!@#", 200, {"id": "wf-!@#", "alias": "Special Workflow", "status": "started"}),
        ("", 200, {"id": "", "alias": "Empty ID", "status": "started"}),
        ("wf-über", 200, {"id": "wf-über", "alias": "Unicode Workflow", "status": "started"}),
    ],
)
def test_get_workflow_success(workflow_id, expected_status, expected_body):
    """
    Test /api/v1/workflows/{workflow_id} with valid mocked dependencies and edge-case IDs.
    'id' is opaque; 'alias' is business-meaningful. Validates JSON-LD @context.
    """

    class DummyEngine:
        def __init__(self):
            self.workflow_repo = DummyWorkflowRepo()

        def start_workflow(self, workflow_id) -> Optional[WorkflowDict]:
            return self.workflow_repo.get_workflow(workflow_id)

    app.container.engine.override(DummyEngine())
    client = TestClient(app)
    response = client.get(f"/api/v1/workflows/{workflow_id}")
    assert response.status_code == expected_status
    data = response.json()
    # Validate JSON-LD @context
    assert "@context" in data
    assert data["@context"]["@vocab"] == "https://schema.org/"
    assert data["@context"]["id"] == "@id"
    assert data["@context"]["alias"] == "rdfs:label"
    assert data["@context"]["status"] == "schema:status"
    # Validate workflow fields
    for k, v in expected_body.items():
        assert data[k] == v



@pytest.mark.parametrize(
    "workflow_id,expected_detail",
    [
        ("does-not-exist", "Workflow not found"),
        ("wf-404", "Workflow not found"),
        ("nonexistent", "Workflow not found"),
    ],
)
def test_get_workflow_not_found(workflow_id, expected_detail):
    """
    Test /api/v1/workflows/{workflow_id} with a non-existent workflow (simulate 404).
    Ensures @context is not present.
    """

    class DummyEngine:
        def __init__(self):
            self.workflow_repo = DummyWorkflowRepo()

        def start_workflow(self, workflow_id) -> Optional[WorkflowDict]:
            result = self.workflow_repo.get_workflow(workflow_id)
            if result is None:
                from fastapi import HTTPException
                raise HTTPException(status_code=404, detail="Workflow not found")
            return result

    app.container.engine.override(DummyEngine())
    client = TestClient(app)
    response = client.get(f"/api/v1/workflows/{workflow_id}")
    assert response.status_code == 404
    data = response.json()
    assert "@context" not in data
    assert data["detail"] == expected_detail



@pytest.mark.parametrize(
    "workflow_id,exc_msg",
    [
        ("wf-error", "Engine failure"),
        ("wf-crash", "Engine failure"),
    ],
)
def test_get_workflow_engine_error(workflow_id, exc_msg):
    """
    Test /api/v1/workflows/{workflow_id} when the engine raises an exception (simulate 500).
    Ensures @context is not present.
    """

    class DummyEngine:
        def __init__(self):
            self.workflow_repo = DummyWorkflowRepo()

        def start_workflow(self, workflow_id) -> Optional[WorkflowDict]:
            raise RuntimeError(exc_msg)

    app.container.engine.override(DummyEngine())
    client = TestClient(app)
    response = client.get(f"/api/v1/workflows/{workflow_id}")
    assert response.status_code == 500
    data = response.json()
    assert "@context" not in data
    assert exc_msg in response.text



@pytest.mark.parametrize(
    "workflow_id",
    ["wf-missing-repo", "wf-none", "wf-null"],
)
def test_get_workflow_missing_repo(workflow_id):
    """
    Test /api/v1/workflows/{workflow_id} when the workflow_repo is missing (simulate 500).
    Ensures @context is not present and error is clear.
    """

    class DummyEngine:
        def __init__(self):
            self.workflow_repo = None

        def start_workflow(self, workflow_id) -> Optional[WorkflowDict]:
            # This will trigger the defensive check in OrchestrationEngine
            return OrchestrationEngine(self.workflow_repo).start_workflow(workflow_id)

    app.container.engine.override(DummyEngine())
    client = TestClient(app)
    response = client.get(f"/api/v1/workflows/{workflow_id}")
    assert response.status_code == 500
    data = response.json()
    assert "@context" not in data
    assert "WorkflowRepositoryPort is not configured" in response.text



def validate_jsonld_against_schema(jsonld_obj):
    """
    Stub for validating JSON-LD against a SHACL/OWL schema.
    In a real system, use pySHACL or rdflib to validate against an ontology file.
    """
    # Example: from pyshacl import validate
    # result = validate(data_graph, shacl_graph=shacl_schema)
    # assert result[0] is True, result[2]
    pass
