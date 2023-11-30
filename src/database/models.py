from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base


class Product(Base):
    __tablename__ = 'product'

    product_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fish: Mapped[str] = mapped_column(String(32), nullable=False)
    cutting: Mapped[str] = mapped_column(String(32), nullable=False)
    producer: Mapped[str] = mapped_column(String(32), nullable=False)
    package: Mapped[str] = mapped_column(String(32), nullable=False)
    weight: Mapped[int] = mapped_column(nullable=False)
