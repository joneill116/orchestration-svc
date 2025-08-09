
"""
Interface/port definitions for orchestration service.
Defines contracts for workflow persistence and retrieval.
Follows the Dependency Inversion Principle for testability and extensibility.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TypedDict
try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated
class WorkflowDict(TypedDict, total=False):
    """
    Explicit contract for workflow objects returned by the repository port.
    'id' is an opaque identifier; 'alias' is business-meaningful.
    OpenAPI field descriptions and x-ontology annotations are provided via Annotated.
    """
    id: Annotated[
        str,
        {
            "description": "Opaque workflow identifier (not business-meaningful)",
            "x-ontology": "@id"
        }
    ]
    alias: Annotated[
        Optional[str],
        {
            "description": "Business-meaningful alias or label for the workflow",
            "x-ontology": "rdfs:label"
        }
    ]
    status: Annotated[
        str,
        {
            "description": "Current status of the workflow",
            "x-ontology": "schema:status"
        }
    ]
    # Add more fields as needed, using Annotated for OpenAPI/x-ontology

class WorkflowRepositoryPort(ABC):
    """
    Port for workflow persistence and retrieval.
    Implementations should handle storage and retrieval of workflow data.
    """
    @abstractmethod

    def get_workflow(self, workflow_id: str) -> Optional[WorkflowDict]:
        """
        Retrieve a workflow by its opaque ID.
        :param workflow_id: The workflow identifier (opaque)
        :return: The workflow data as a WorkflowDict (with 'id', 'alias', etc.), or None if not found.
        Supports both sync and async implementations.
        Logging and error handling should be consistent and observable.
        """
        pass

    @abstractmethod
    def save_workflow(self, workflow: WorkflowDict) -> bool:
        """
        Persist a workflow.
        :param workflow: The workflow data as a WorkflowDict
        :return: True if saved successfully, False otherwise
        """
        pass

# Add more ports as needed for orchestration logic
