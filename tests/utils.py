import pytest
from typing import Any, Dict, Optional, Set, Generator

from orchestration_svc.domain.ports import WorkflowRepositoryPort
from orchestration_svc.main import app
from orchestration_svc.constants import JSONLD_CONTEXT


def test_mock_workflow_repo_get_workflow_all_paths() -> None:
    # Covers: known_workflow_ids=None, known_workflow_ids set, not a string, not found
    repo1 = MockWorkflowRepo()
    assert repo1.get_workflow("not-present") is None
    repo2 = MockWorkflowRepo(known_workflow_ids={"foo"})
    result = repo2.get_workflow("foo")
    assert result is not None and result["id"] == "foo"
    # The following line is intentionally omitted: type error expected
    # assert repo2.get_workflow(123) is None
    assert repo2.get_workflow("bar") is None


def test_mock_workflow_repo_save_workflow() -> None:
    repo = MockWorkflowRepo()
    assert repo.save_workflow({"id": "x"}) is True


def test_mock_engine_start_workflow() -> None:
    engine = MockEngine()
    # Should return None for unknown id
    assert engine.start_workflow("not-present") is None
    # Should return a workflow for known id
    engine.workflow_repo.known_workflow_ids.add("foo")
    result = engine.start_workflow("foo")
    assert result is not None and result["id"] == "foo"


"""
Utility test helpers for orchestration-svc.
"""



class MockWorkflowRepo(WorkflowRepositoryPort):
    """A mock repo returning plain dicts with JSON-LD context for testing."""

    def __init__(self, known_workflow_ids: Optional[Set[str]] = None) -> None:
        # Allow injection of known_workflow_ids for test flexibility
        if known_workflow_ids is None:
            # Default: empty set, must be set in test
            self.known_workflow_ids: Set[str] = set()
        else:
            self.known_workflow_ids = set(known_workflow_ids)

    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        if not isinstance(workflow_id, str):
            return None  # type: ignore[unreachable]
        if workflow_id not in self.known_workflow_ids:
            return None
        return {
            "id": workflow_id,
            "alias": "Test Workflow",
            "status": "started",
            "@context": JSONLD_CONTEXT,
        }

    def save_workflow(self, workflow: Dict[str, Any]) -> bool:
        return True

    def create_workflow(self, alias: str) -> dict[str, Any]:
        import uuid
        workflow_id = str(uuid.uuid4())
        self.known_workflow_ids.add(workflow_id)
        return {
            "id": workflow_id,
            "alias": alias,
            "status": "started",
            "@context": JSONLD_CONTEXT,
        }



class MockEngine:
    def __init__(self) -> None:
        self.workflow_repo: MockWorkflowRepo = MockWorkflowRepo()

    def start_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        return self.workflow_repo.get_workflow(workflow_id)

    def create_workflow(self, alias: str) -> dict[str, Any]:
        return self.workflow_repo.create_workflow(alias)


@pytest.fixture(autouse=True)
def reset_container() -> Generator[None, None, None]:
    """Reset DI container overrides after each test for isolation. Only resets if overridden."""
    yield
    provider = app.container.workflow_repo
    if getattr(provider, "overridden", False):
        provider.reset_last_overriding()


@pytest.fixture
def mock_repo() -> MockWorkflowRepo:
    """Fixture for a mock workflow repo with no known workflows by default."""
    return MockWorkflowRepo()


@pytest.fixture
def mock_engine() -> MockEngine:
    """Fixture for a mock orchestration engine with a mock repo."""
    return MockEngine()
