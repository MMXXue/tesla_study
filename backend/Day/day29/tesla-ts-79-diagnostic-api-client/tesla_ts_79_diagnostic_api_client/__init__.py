"""A client library for accessing Tesla TS-79 Diagnostic API"""

from .client import AuthenticatedClient, Client

__all__ = (
    "AuthenticatedClient",
    "Client",
)
