from typing import Any, Dict, List, Optional, Sequence

from weaviate.classes.config import Configure, DataType, Property, Tokenization

VECTOR_INDEX_TYPES = {
    "hnsw": Configure.VectorIndex.hnsw,
    "flat": Configure.VectorIndex.flat,
    "dynamic": Configure.VectorIndex.dynamic,
}


def build_inverted_index(config: Optional[Dict[str, Any]]):
    if config is None:
        return None
    if not isinstance(config, dict):
        raise TypeError("inverted_index_config must be a dict")
    return Configure.inverted_index(**config)


def build_vector_index(index_type: Optional[str]):
    if index_type is None:
        return None
    if not isinstance(index_type, str):
        raise TypeError("vector_index_config must be a string")
    key = index_type.strip().lower()
    if key not in VECTOR_INDEX_TYPES:
        raise ValueError(
            f"Invalid vector index '{index_type}'. "
            f"Allowed values: {', '.join(VECTOR_INDEX_TYPES)}"
        )
    return VECTOR_INDEX_TYPES[key]()


def build_properties(props: Optional[List[Dict[str, Any]]]) -> Optional[Sequence[Property]]:
    if props is None:
        return None
    if not isinstance(props, list):
        raise TypeError("properties must be a list of dicts")

    result = []
    for i, p in enumerate(props):
        if not isinstance(p, dict):
            raise TypeError(f"properties[{i}] must be a dict")
        if "name" not in p or "data_type" not in p:
            raise ValueError(f"properties[{i}] needs 'name' and 'data_type'")

        try:
            data_type = DataType(str(p["data_type"]).lower())
        except ValueError:
            allowed = ", ".join(d.value for d in DataType)
            raise ValueError(
                f"properties[{i}] has invalid data_type '{p['data_type']}'. Allowed: {allowed}"
            )

        extra = {k: v for k, v in p.items() if k not in ("name", "data_type", "tokenization")}
        if "tokenization" in p:
            try:
                extra["tokenization"] = Tokenization(str(p["tokenization"]).lower())
            except ValueError:
                allowed = ", ".join(t.value for t in Tokenization)
                raise ValueError(
                    f"properties[{i}] has invalid tokenization '{p['tokenization']}'. Allowed: {allowed}"
                )

        result.append(Property(name=p["name"], data_type=data_type, **extra))
    return result