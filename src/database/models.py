from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import String, Text, func, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base
from src.transaction.schemas import TransactionType


class Product(Base):
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fish: Mapped[str] = mapped_column(String(32), nullable=False)
    cutting: Mapped[str] = mapped_column(String(32), nullable=False)
    producer: Mapped[str] = mapped_column(String(32), nullable=False)
    package: Mapped[str] = mapped_column(String(32), nullable=False)
    weight: Mapped[int] = mapped_column(Integer, nullable=False)


class Contractor(Base):
    contractor_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)


class Transaction(Base):
    transaction_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    transaction_type: Mapped[str] = mapped_column(String(16), nullable=False)
    contractor_id: Mapped[int] = mapped_column(ForeignKey("contractor.contractor_id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.product_id", ondelete="CASCADE"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    note: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(nullable=True)


class Email(Base):
    email_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    contractor_id: Mapped[int] = mapped_column(ForeignKey("contractor.contractor_id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False)


class Phone(Base):
    phone_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    contractor_id: Mapped[int] = mapped_column(ForeignKey("contractor.contractor_id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    phone: Mapped[str] = mapped_column(String(64), nullable=False)
