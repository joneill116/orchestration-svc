

# Standard library
from typing import Optional

# Third-party
import pytest
from fastapi.testclient import TestClient

# Local imports
from orchestration_svc.engine.core import OrchestrationEngine
from orchestration_svc.main import app


from .utils import MockWorkflowRepo
import uuid




# Use fixture to reset DI container overrides after each test for isolation
@pytest.fixture(autouse=True)
def reset_container():
    yield
    app.container.workflow_repo.reset_last_overriding()



@pytest.mark.parametrize(
    "workflow_id,expected_status,expected_body",
    [
        (str(uuid.uuid4()), 200, lambda wid: {"id": wid, "alias": "Test Workflow", "status": "started"}),
        (str(uuid.uuid4()), 200, lambda wid: {"id": wid, "alias": "Test Workflow", "status": "started"}),
    ],
)
def test_get_workflow_success(workflow_id, expected_status, expected_body):
    """
    Test /api/v1/workflows/{workflow_id} with valid mocked dependencies and edge-case IDs.
    'id' is opaque; 'alias' is business-meaningful. Validates JSON-LD @context.
    """
    app.container.workflow_repo.override(MockWorkflowRepo(known_workflow_ids={workflow_id}))
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
    for k, v in expected_body(workflow_id).items():
        assert data[k] == v



@pytest.mark.parametrize(
    "workflow_id,expected_detail",
    [
        (str(uuid.uuid4()), "Workflow not found"),
        (str(uuid.uuid4()), "Workflow not found"),
    ],
)
def test_get_workflow_not_found(workflow_id, expected_detail):
    """
    Test /api/v1/workflows/{workflow_id} with a non-existent workflow (simulate 404).
    Ensures @context is not present.
    """
    app.container.workflow_repo.override(MockWorkflowRepo(known_workflow_ids=set()))
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
    class ErrorRepo:
        def get_workflow(self, workflow_id):
            raise RuntimeError(exc_msg)
    app.container.workflow_repo.override(ErrorRepo())
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
    app.container.workflow_repo.override(None)
    client = TestClient(app)
    response = client.get(f"/api/v1/workflows/{workflow_id}")
    assert response.status_code == 500
    data = response.json()
    assert "@context" not in data
    assert "Workflow repository is not configured in OrchestrationEngine" in response.text



def validate_jsonld_against_schema(jsonld_obj):
    """
    Stub for validating JSON-LD against a SHACL/OWL schema.
    In a real system, use pySHACL or rdflib to validate against an ontology file.
    """
    # Example: from pyshacl import validate
    # result = validate(data_graph, shacl_graph=shacl_schema)
    # assert result[0] is True, result[2]
    pass
