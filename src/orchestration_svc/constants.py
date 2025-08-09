"""
Shared constants for orchestration-svc.
Includes JSON-LD context and error schemas for DRYness and clarity.
"""

# Shared JSON-LD context for all workflow responses
from typing import Dict, Any

JSONLD_CONTEXT: Dict[str, str] = {
    "@vocab": "https://schema.org/",
    "id": "@id",
    "alias": "rdfs:label",
    "status": "schema:status",
}


def get_error_schema() -> Dict[str, Any]:
    """
    Returns the shared error schema for OpenAPI and error responses.
    This is a function for future extensibility (e.g., parameterized error schemas).
    """
    return {
        "type": "object",
        "properties": {
            "error": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "example": "WORKFLOW_NOT_FOUND"},
                    "message": {"type": "string", "example": "Workflow not found"},
                    "detail": {
                        "type": "string",
                        "example": "Extra error details (optional)",
                    },
                },
                "required": ["code", "message"],
            }
        },
        "required": ["error"],
    }
