import pytest
from fastapi.testclient import TestClient
from orchestration_svc.main import app
from .utils import MockWorkflowRepo
from typing import Generator, Any

"""
API contract test for orchestration-svc.
Ensures the /api/v1/workflows/{workflow_id} endpoint returns the expected schema and headers.
"""


@pytest.fixture(autouse=True)
def reset_container() -> Generator[Any, None, None]:
    yield
    app.container.workflow_repo.reset_last_overriding()


def test_get_workflow_contract() -> None:
    # Inject dummy engine into the app's container
    app.container.workflow_repo.override(
        MockWorkflowRepo(known_workflow_ids={"wf-contract"})
    )
    client = TestClient(app)
    workflow_id = "wf-contract"
    response = client.get(
        f"/api/v1/workflows/{workflow_id}", headers={"x-correlation-id": "test-corr-id"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == workflow_id
    assert "status" in data
    # Check correlation ID propagation
    assert response.headers["x-correlation-id"] == "test-corr-id"
