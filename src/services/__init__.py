"""Logic package."""

from services.store import (
    get_store_url,
    get_data_from_store,
    create_or_update_product_from_store,
)

__all__ = [
    "get_data_from_store",
    "get_store_url",
    "create_or_update_product_from_store",
]
