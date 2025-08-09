
"""
Dependency injection container for orchestration-svc.
Wires up only orchestration logic and interfaces/ports—no adapters or business logic.
"""

from dependency_injector import containers, providers
from orchestration_svc.engine.core import OrchestrationEngine
from orchestration_svc.domain.ports import WorkflowRepositoryPort

class Container(containers.DeclarativeContainer):
    """
    DI container for orchestration-svc.
    All dependencies are injected for testability and microservice clarity.
    """
    wiring_config = containers.WiringConfiguration(modules=["orchestration_svc.api.routes"])

    # Example: workflow_repo = providers.Singleton(YourWorkflowRepoImpl)
    workflow_repo = providers.Object(None)  # Replace with real implementation
    engine = providers.Singleton(OrchestrationEngine, workflow_repo=workflow_repo)
