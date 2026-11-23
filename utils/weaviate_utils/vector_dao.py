import weaviate
from weaviate.auth import Auth


from utils.constants import (
    WEAVIATE_HOST,
    WEAVIATE_HTTP_PORT,
    WEAVIATE_GRPC_PORT,
    WEAVIATE_SECURE,
    WEAVIATE_API_KEY,
)


class VectorDAO:
    """Data access object for Weaviate. The client is created when the class is instantiated."""

    def __init__(self):
        self.client = weaviate.connect_to_custom(
            http_host=WEAVIATE_HOST,
            http_port=WEAVIATE_HTTP_PORT,
            http_secure=WEAVIATE_SECURE,
            grpc_host=WEAVIATE_HOST,
            grpc_port=WEAVIATE_GRPC_PORT,
            grpc_secure=WEAVIATE_SECURE,
            auth_credentials=Auth.api_key(WEAVIATE_API_KEY) if WEAVIATE_API_KEY else None,
        )

    def close(self):
        """Close the connection to Weaviate."""
        self.client.close()

    def create_collection(self, name, properties=None, vector_config=None, description=None):
        if self.client.collections.exists(name):
            return self.client.collections.get(name)

        return self.client.collections.create(
            name=name,
            description=description,
            properties=properties
        )