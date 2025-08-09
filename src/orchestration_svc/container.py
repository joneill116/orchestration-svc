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

    wiring_config = containers.WiringConfiguration(
        modules=["orchestration_svc.api.routes"]
    )

    # DI provider for the workflow repository port. Overridden in tests and deployments.
    # None by default for testability and to enforce explicit configuration.
    workflow_repo: providers.Provider[Optional[WorkflowRepositoryPort]] = (
        providers.Object(None)
    )

    # DI provider for the orchestration engine, always injected with the current workflow_repo.
    engine: providers.Provider[OrchestrationEngine] = providers.Factory(
        OrchestrationEngine,
        workflow_repo=workflow_repo,
    )

    def check_runtime_config(self) -> None:
        """
        Raise an error if workflow_repo is None in a non-test environment.
        Call this in production startup to enforce explicit configuration.
        """
        if self.workflow_repo() is None:
            raise RuntimeError(
                "workflow_repo must be configured in production. "
                "Override the provider with a real implementation."
            )

    # TODO: In production, add security/auth providers here (e.g., JWT, OAuth2) as needed.
