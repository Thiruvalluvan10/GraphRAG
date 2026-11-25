import weaviate
from weaviate.auth import Auth
from weaviate.collections.classes.config import Configure
from weaviate.exceptions import WeaviateBaseError

from weaviate_db.exception import WeaviateCollectionCreateError
from weaviate_db.utils import build_inverted_index, build_properties, build_vector_index

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

    def create_collection(
            self,
            name: str,
            description: str = None,
            inverted_index_config: dict = None,
            multi_tenancy_config: bool = False,
            properties: list = None,
            vector_index_config: str = None,
    ):
        try:
            if self.client.collections.exists(name):
                raise WeaviateCollectionCreateError(
                    f"Collection '{name}' already exists", name
                )

            return self.client.collections.create(
                name=name,
                description=description,
                inverted_index_config=build_inverted_index(inverted_index_config),
                multi_tenancy_config=Configure.multi_tenancy(enabled=multi_tenancy_config),
                properties=build_properties(properties),
                replication_config=Configure.replication(factor=2),
                sharding_config=Configure.sharding(desired_count=2),
                vector_index_config=build_vector_index(vector_index_config),
            )
        except WeaviateCollectionCreateError:
            raise
        except (ValueError, TypeError) as e:
            raise WeaviateCollectionCreateError(
                f"Invalid configuration for collection '{name}': {e}", name
            ) from e
        except WeaviateBaseError as e:
            raise WeaviateCollectionCreateError(
                f"Failed to create collection '{name}': {e}", name
            ) from e