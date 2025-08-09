import pytest

"""
API contract test for orchestration-svc.
Ensures the /api/v1/workflows/{workflow_id} endpoint returns the expected schema and headers.
"""

@pytest.fixture(autouse=True)
def reset_container():
    yield
    app.container.engine.reset_last_overriding()

from fastapi.testclient import TestClient
from orchestration_svc.main import app

class DummyWorkflowRepo:
    def get_workflow(self, workflow_id):
        return {"id": workflow_id, "status": "started"}

class DummyEngine:
    def __init__(self):
        self.workflow_repo = DummyWorkflowRepo()
    def start_workflow(self, workflow_id):
        return self.workflow_repo.get_workflow(workflow_id)

def test_get_workflow_contract():
    # Inject dummy engine into the app's container
    app.container.engine.override(DummyEngine())
    client = TestClient(app)
    workflow_id = "wf-contract"
    response = client.get(f"/api/v1/workflows/{workflow_id}", headers={"x-correlation-id": "test-corr-id"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == workflow_id
    assert "status" in data
    # Check correlation ID propagation
    assert response.headers["x-correlation-id"] == "test-corr-id"
