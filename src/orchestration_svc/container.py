
"""
Dependency injection container for orchestration-svc.
Wires up only orchestration logic and interfaces/ports—no adapters or business logic.
"""

from dependency_injector import containers, providers
from orchestration_svc.engine.core import OrchestrationEngine


class Container(containers.DeclarativeContainer):
    """
    DI container for orchestration-svc.
    All dependencies are injected for testability and microservice clarity.
    """
    wiring_config = containers.WiringConfiguration(modules=["orchestration_svc.api.routes"])

    # All adapters/integrations are externalized; workflow_repo is a placeholder
    workflow_repo = providers.Object(None)  # Externalized in real deployments
    engine = providers.Factory(OrchestrationEngine, workflow_repo=workflow_repo)
