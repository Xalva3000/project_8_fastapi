from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict
from src.product.schemas import Product
from src.contractor.schemas import Contractor


class TransactionType(Enum):
    INCOME = 'income'
    OUTCOME = 'outcome'


class TransactionBase(BaseModel):
    transaction_id: int
    transaction_type: TransactionType
    contractor_id: int
    product_id: int
    quantity: int
    note: str | None
    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class TransactionUpdatePartial(TransactionBase):
    transaction_id: int | None = None
    transaction_type: str | None = None
    contractor_id: int | None = None
    product_id: int | None = None
    quantity: int | None = None
    note: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class Transaction(TransactionBase):
    model_config = ConfigDict(from_attributes=True)

    transaction_id: int
