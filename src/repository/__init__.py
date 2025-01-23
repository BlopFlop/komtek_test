"""Repositories package."""

from repository.product import get_product_repository, ProductRepository
from repository.base import RepositoryBase

__all__ = ["ProductRepository", "RepositoryBase", "get_product_repository"]
