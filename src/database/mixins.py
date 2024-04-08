from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.database.models import Product


class ProductRelationMixin:
    _product_id_unique: bool = False
    _product_id_primary_key: bool = False
    _product_back_populates: str | None = False

    @declared_attr
    def product_id(cls) -> Mapped[int]:
        return mapped_column(ForeignKey("product.product_id"),
                             primary_key=cls._product_id_primary_key,
                             unique=cls._product_id_unique)

    @declared_attr
    def product(cls) -> Mapped["Product"]:
        return relationship("Product",
                            back_populates=cls._product_back_populates)
