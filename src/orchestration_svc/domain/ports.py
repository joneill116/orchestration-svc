

"""
Ports/interfaces for orchestration-svc.
Defines the WorkflowRepositoryPort Protocol for type safety.
All adapters and domain models are externalized.
"""

from typing import Protocol, Optional, Dict, Any

class WorkflowRepositoryPort(Protocol):
    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        ...
    def save_workflow(self, workflow: Dict[str, Any]) -> bool:
        ...
