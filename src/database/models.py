from datetime import datetime, date

from sqlalchemy import String, Text, func, Integer, ForeignKey, DateTime, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.mixins import ProductRelationMixin

from src.database.base import Base


class Product(Base):
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fish: Mapped[str] = mapped_column(String(32), nullable=False)
    cutting: Mapped[str] = mapped_column(String(32), nullable=False)
    size: Mapped[str] = mapped_column(String(32), nullable=True)
    producer: Mapped[str] = mapped_column(String(32), nullable=False)
    package: Mapped[str] = mapped_column(String(32), nullable=False)
    weight: Mapped[int] = mapped_column(Integer, nullable=False)

    specifications: Mapped[list["Specification"]] = relationship(back_populates="product")
    storage: Mapped["StorageItem"] = relationship(back_populates="product")

    def __repr__(self):
        return f'{self.product_id}id {self.fish} {self.cutting} {self.size} ' \
               f'"{self.producer}" ({self.package}) {self.weight}кг'


class Contractor(Base):
    contractor_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)

    contracts: Mapped[list["Contract"]] = relationship(back_populates='contractor')

    def __repr__(self):
        return f'{self.contractor_id}id {self.name} {self.address}'


class Contract(Base):
    contract_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    contract_type: Mapped[str] = mapped_column(String(16), nullable=False)
    planned_date: Mapped[date] = mapped_column(DateTime,
                                               server_default=text("CURRENT_DATE"),
                                               default=date.today)
    reserved: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    payment: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    executed: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    note: Mapped[str] = mapped_column(Text, nullable=True, server_default=None, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime,
                                                 server_default=text("TIMEZONE('utc', now())"),
                                                 default=datetime.utcnow)
    executed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    contractor_id: Mapped[int] = mapped_column(ForeignKey("contractor.contractor_id", ondelete="CASCADE"))
    contractor: Mapped["Contractor"] = relationship("Contractor", back_populates="contracts")
    specifications: Mapped[list["Specification"]] = relationship(back_populates='contract')

    def __repr__(self):
        return f"{self.contract_id} {self.contract_type} {self.contract_id} {self.reserved} {self.payment} {self.executed}"


class Specification(Base, ProductRelationMixin):
    _relation_back_populates = 'specifications'
    spec_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    quantity: Mapped[int] = mapped_column(Integer, default="0", server_default="0", nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=True, server_default=None, default=None)

    product_id: Mapped[int] = mapped_column(ForeignKey("product.product_id", ondelete="CASCADE"))
    contract_id: Mapped[int] = mapped_column(ForeignKey("contract.contract_id", ondelete="CASCADE"))

    product: Mapped["Product"] = relationship("Product", back_populates=_relation_back_populates)
    contract: Mapped["Contract"] = relationship("Contract", back_populates=_relation_back_populates)

    def __repr__(self):
        return f"{self.spec_id}id {self.product_id} {self.quantity} {self.price}"


class StorageItem(Base, ProductRelationMixin):
    _product_back_populates = 'storage'
    _product_id_primary_key = True

    available: Mapped[int] = mapped_column(Integer, default="0", server_default="0", nullable=False)
    owned: Mapped[int] = mapped_column(Integer, default="0", server_default="0", nullable=False)
    stored: Mapped[int] = mapped_column(Integer, default="0", server_default="0", nullable=False)

    def __repr__(self):
        return f"{self.product_id}: {self.available}(available), {self.owned}(owned), {self.stored}(stored)"


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
