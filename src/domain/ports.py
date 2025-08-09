# Interface/port definitions for orchestration service

from abc import ABC, abstractmethod

class WorkflowRepositoryPort(ABC):
    @abstractmethod
    def get_workflow(self, workflow_id: str):
        pass

    @abstractmethod
    def save_workflow(self, workflow):
        pass

# Add more ports as needed for orchestration logic
