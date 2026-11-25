"""Custom exceptions that inherit from the actual Weaviate exceptions."""

from weaviate.exceptions import (
    WeaviateBaseError,
    WeaviateConnectionError,
    WeaviateQueryError,
    WeaviateTimeoutError,
)


class WeaviateCustomError(WeaviateBaseError):
    """Custom base exception for all Weaviate related errors in this project."""

    def __init__(self, message: str = ""):
        super().__init__(message)


class WeaviateConnectionFailedError(WeaviateConnectionError):
    """Raised when the connection to Weaviate fails."""

    def __init__(self, message: str = ""):
        super().__init__(message)


class WeaviateQueryFailedError(WeaviateQueryError):
    """Raised when a Weaviate query fails."""

    def __init__(self, message: str, protocol_type: str = "REST"):
        super().__init__(message, protocol_type)


class WeaviateTimeoutError(WeaviateTimeoutError):
    """Raised when a request to Weaviate times out."""

    def __init__(self, message: str = ""):
        super().__init__(message)

class WeaviateCollectionCreateError(WeaviateBaseError):
    """Raised when creating a collection fails."""
    def __init__(self, message: str = "", collection_name: str = None):
        self.collection_name = collection_name
        super().__init__(message)