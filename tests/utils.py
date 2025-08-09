import pytest
# ...existing code...

def test_mock_workflow_repo_get_workflow_all_paths():
    # Covers: known_workflow_ids=None, known_workflow_ids set, not a string, not found
    repo1 = MockWorkflowRepo()
    assert repo1.get_workflow("not-present") is None
    repo2 = MockWorkflowRepo(known_workflow_ids={"foo"})
    assert repo2.get_workflow("foo")["id"] == "foo"
    assert repo2.get_workflow(123) is None
    assert repo2.get_workflow("bar") is None

def test_mock_workflow_repo_save_workflow():
    repo = MockWorkflowRepo()
    assert repo.save_workflow({"id": "x"}) is True

def test_mock_engine_start_workflow():
    engine = MockEngine()
    # Should return None for unknown id
    assert engine.start_workflow("not-present") is None
    # Should return a workflow for known id
    engine.workflow_repo.known_workflow_ids.add("foo")
    result = engine.start_workflow("foo")
    assert result["id"] == "foo"
"""
Shared test utilities and fixtures for orchestration-svc tests.
Provides reusable dummy repositories, engines, and fixtures for test isolation and clarity.
"""

from typing import Any, Dict, Optional
from orchestration_svc.domain.ports import WorkflowRepositoryPort
import pytest
from orchestration_svc.engine.core import OrchestrationEngine
from orchestration_svc.main import app


class MockWorkflowRepo(WorkflowRepositoryPort):
    """A mock repo returning plain dicts with JSON-LD context for testing."""
    def __init__(self, known_workflow_ids=None):
        # Allow injection of known_workflow_ids for test flexibility
        if known_workflow_ids is None:
            # Default: empty set, must be set in test
            self.known_workflow_ids = set()
        else:
            self.known_workflow_ids = set(known_workflow_ids)

    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        jsonld_context = {
            "@vocab": "https://schema.org/",
            "id": "@id",
            "alias": "rdfs:label",
            "status": "schema:status",
        }
        if not isinstance(workflow_id, str):
            return None
        if workflow_id in self.known_workflow_ids:
            return {
                "id": workflow_id,
                "alias": "Test Workflow",
                "status": "started",
                "@context": jsonld_context,
            }
        return None

    def save_workflow(self, workflow: Dict[str, Any]) -> bool:
        return True


class MockEngine:
    def __init__(self):
        self.workflow_repo = MockWorkflowRepo()
    def start_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        return self.workflow_repo.get_workflow(workflow_id)


@pytest.fixture(autouse=True)
def reset_container():
    """Reset DI container overrides after each test for isolation. Only resets if overridden."""
    yield
    provider = app.container.workflow_repo
    if getattr(provider, "overridden", False):
        provider.reset_last_overriding()


@pytest.fixture
def mock_repo():
    """Fixture for a mock workflow repo with no known workflows by default."""
    return MockWorkflowRepo()


@pytest.fixture
def mock_engine():
    """Fixture for a mock orchestration engine with a mock repo."""
    return MockEngine()
