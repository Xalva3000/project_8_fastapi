from datetime import datetime, date
from sqlalchemy import String, Text, func, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
# from src.contract.schemas import ContractType

from src.database.base import Base


class Product(Base):
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fish: Mapped[str] = mapped_column(String(32), nullable=False)
    cutting: Mapped[str] = mapped_column(String(32), nullable=False)
    size: Mapped[str] = mapped_column(String(32), nullable=True)
    producer: Mapped[str] = mapped_column(String(32), nullable=False)
    package: Mapped[str] = mapped_column(String(32), nullable=False)
    weight: Mapped[int] = mapped_column(Integer, nullable=False)


class Contractor(Base):
    contractor_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)


class Contract(Base):
    contract_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    contract_type: Mapped[str] = mapped_column(String(16), nullable=False)
    contractor_id: Mapped[int] = mapped_column(ForeignKey("contractor.contractor_id", ondelete="CASCADE"))
    payment: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    executed: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    note: Mapped[str] = mapped_column(Text, nullable=True, server_default=None, default=None)


class Specification(Base):
    spec_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    contract_id: Mapped[int] = mapped_column(ForeignKey("contract.contract_id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.product_id", ondelete="CASCADE"))
    quantity: Mapped[int] = mapped_column(Integer, default="0", server_default="0", nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=True, server_default=None, default=None)


# class Possession(Base):
#     possession_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     product_id: Mapped[int] = mapped_column(ForeignKey("product.product_id"))
#     quantity: Mapped[int] = mapped_column(Integer, default="0", server_default="0", nullable=False)

class Possession(Base):
    product_id: Mapped[int] = mapped_column(ForeignKey("product.product_id"), primary_key=True, unique=True)
    quantity: Mapped[int] = mapped_column(Integer, default="0", server_default="0", nullable=False)


class Storage(Base):
    product_id: Mapped[int] = mapped_column(ForeignKey("product.product_id"), primary_key=True, unique=True)
    quantity: Mapped[int] = mapped_column(Integer, default="0", server_default="0", nullable=False)


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
