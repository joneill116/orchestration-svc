
"""
Minimal configuration for orchestration-svc.
Only orchestration-specific settings are included.
All environment/config management is externalized in a microservice ecosystem.
"""

from typing import Final

class Settings:
    """
    Configuration for orchestration-svc.
    Only orchestration-specific settings are defined here.
    """
    API_PREFIX: Final[str] = "/api"
    PROJECT_NAME: Final[str] = "orchestration-svc"

settings = Settings()
