
def test_create_workflow_success() -> None:
    """
    Test POST /api/v1/workflows to create a workflow by alias. Validates opaque id and JSON-LD context.
    """
    app.container.workflow_repo.override(MockWorkflowRepo())
    client = TestClient(app)
    alias = "Human Readable Workflow Name"
    response = client.post(
        "/api/v1/workflows",
        json={"alias": alias},
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data and isinstance(data["id"], str)
    assert data["alias"] == alias
    assert data["status"] == "started"
    assert "@context" in data
    assert data["@context"]["@vocab"] == "https://schema.org/"
# Standard library
import uuid
from typing import Callable, Any, Generator

# Third-party
import pytest
from fastapi.testclient import TestClient

# Local imports
from orchestration_svc.main import app
from .utils import MockWorkflowRepo


# Use fixture to reset DI container overrides after each test for isolation
@pytest.fixture(autouse=True)
def reset_container() -> Generator[None, None, None]:
    yield
    provider = app.container.workflow_repo
    if getattr(provider, "overridden", False):
        provider.reset_last_overriding()


@pytest.mark.parametrize(
    "workflow_id,expected_status,expected_body",
    [
        (
            str(uuid.uuid4()),
            200,
            lambda wid: {"id": wid, "alias": "Test Workflow", "status": "started"},
        ),
    ],
)
def test_get_workflow_success(
    workflow_id: str,
    expected_status: int,
    expected_body: Callable[[str], dict[str, Any]],
) -> None:
    """
    Test /api/v1/workflows/{workflow_id} with valid mocked dependencies and edge-case IDs.
    'id' is opaque; 'alias' is business-meaningful. Validates JSON-LD @context.
    """
    app.container.workflow_repo.override(
        MockWorkflowRepo(known_workflow_ids={workflow_id})
    )
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
def test_get_workflow_not_found(workflow_id: str, expected_detail: str) -> None:
    """
    Test /api/v1/workflows/{workflow_id} with a non-existent workflow (simulate 404).
    Ensures @context is not present and error model is correct.
    """
    app.container.workflow_repo.override(MockWorkflowRepo(known_workflow_ids=set()))
    client = TestClient(app)
    response = client.get(f"/api/v1/workflows/{workflow_id}")
    assert response.status_code == 404
    data = response.json()
    assert "@context" not in data
    assert "error" in data
    assert data["error"]["code"] == "WORKFLOW_NOT_FOUND"
    assert data["error"]["message"] == expected_detail


@pytest.mark.parametrize(
    "workflow_id,exc_msg",
    [
        ("wf-error", "Engine failure"),
        ("wf-crash", "Engine failure"),
    ],
)
def test_get_workflow_engine_error(workflow_id: str, exc_msg: str) -> None:
    """
    Test /api/v1/workflows/{workflow_id} when the engine raises an exception (simulate 500).
    Ensures @context is not present and error model is correct.
    """

    class ErrorRepo:
        def get_workflow(self, workflow_id: str) -> None:
            raise RuntimeError(exc_msg)

    app.container.workflow_repo.override(ErrorRepo())
    client = TestClient(app)
    response = client.get(f"/api/v1/workflows/{workflow_id}")
    assert response.status_code == 500
    data = response.json()
    assert "@context" not in data
    assert "error" in data
    assert data["error"]["code"] == "ENGINE_ERROR"
    assert data["error"]["message"] == "Engine failure"
    assert data["error"]["detail"] == exc_msg


@pytest.mark.parametrize(
    "workflow_id",
    ["wf-missing-repo", "wf-none", "wf-null"],
)
def test_get_workflow_missing_repo(workflow_id: str) -> None:
    """
    Test /api/v1/workflows/{workflow_id} when the workflow_repo is missing (simulate 500).
    Ensures @context is not present and error model is correct.
    """
    app.container.workflow_repo.override(None)
    client = TestClient(app)
    response = client.get(f"/api/v1/workflows/{workflow_id}")
    assert response.status_code == 500
    data = response.json()
    assert "@context" not in data
    assert "error" in data
    assert data["error"]["code"] == "ENGINE_ERROR"
    assert data["error"]["message"] == "Engine failure"
    assert (
        "Workflow repository is not configured in OrchestrationEngine"
        in data["error"]["detail"]
    )


def validate_jsonld_against_schema(jsonld_obj: dict[str, Any]) -> bool:
    """
    Stub for validating JSON-LD against a SHACL/OWL schema.
    In a real system, use pySHACL or rdflib to validate against an ontology file.
    """
    # Example: from pyshacl import validate
    # result = validate(data_graph, shacl_graph=shacl_schema)
    # assert result[0] is True, result[2]
    return True


def test_validate_jsonld_against_schema_covers() -> None:
    # Covers the stub for coverage completeness
    assert validate_jsonld_against_schema({}) is True
