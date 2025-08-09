
"""
Dependency injection container for orchestration-svc.
Wires up only orchestration logic and interfaces/ports—no adapters or business logic.
"""


from dependency_injector import containers, providers
from orchestration_svc.engine.core import OrchestrationEngine
from typing import Optional
from orchestration_svc.domain.ports import WorkflowRepositoryPort


class Container(containers.DeclarativeContainer):
    """
    DI container for orchestration-svc.
    All dependencies are injected for testability and microservice clarity.
    Providers are explicitly documented for maintainability and onboarding.
    """
    wiring_config = containers.WiringConfiguration(modules=["orchestration_svc.api.routes"])

    #: DI provider for the workflow repository port. Overridden in tests and deployments.
    #: None by default for testability and to enforce explicit configuration.
    workflow_repo: providers.Provider[Optional[WorkflowRepositoryPort]] = providers.Object(None)  # type: ignore

    #: DI provider for the orchestration engine, always injected with the current workflow_repo.
    engine = providers.Factory(OrchestrationEngine, workflow_repo=workflow_repo)

    # TODO: In production, add security/auth providers here (e.g., JWT, OAuth2) as needed.
