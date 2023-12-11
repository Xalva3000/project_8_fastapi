from enum import Enum

from pydantic import BaseModel, ConfigDict


#
# class ContractType(Enum):
#     INCOME = 'income'
#     OUTCOME = 'outcome'


class ContractBase(BaseModel):
    contract_type: str
    contractor_id: int
    payment: bool = False
    executed: bool = False
    note: str | None


class ContractCreate(ContractBase):
    pass


class ContractUpdate(ContractBase):
    pass


class ContractUpdatePartial(ContractBase):
    contract_type: str | None = None
    contractor_id: int | None = None
    payment: bool | None = None
    executed: bool | None = None
    note: str | None = None


class Contract(ContractBase):
    model_config = ConfigDict(from_attributes=True)
    contract_id: int
