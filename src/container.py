from dependency_injector import containers, providers
from engine.core import OrchestrationEngine
from domain.ports import WorkflowRepositoryPort

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["api.routes"])

    # Example: workflow_repo = providers.Singleton(YourWorkflowRepoImpl)
    workflow_repo = providers.Object(None)  # Replace with real implementation
    engine = providers.Singleton(OrchestrationEngine, workflow_repo=workflow_repo)
