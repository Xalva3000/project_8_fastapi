from datetime import date

from pydantic import BaseModel, ConfigDict


class SpecificationBase(BaseModel):
    contract_id: int
    product_id: int
    quantity: int
    price: int


class SpecificationCreate(SpecificationBase):
    pass


class SpecificationUpdate(SpecificationBase):
    pass


class SpecificationUpdatePartial(SpecificationBase):
    contract_id: int | None = None
    product_id: int | None = None
    quantity: int | None = None
    price: int | None = None


class Specification(SpecificationBase):
    model_config = ConfigDict(from_attributes=True)
    spec_id: int


class ContractSpecificationCreate(BaseModel):
    product_id: int
    quantity: int
    price: int


class ContractSpecificationsCreate(BaseModel):
    specifications: list[ContractSpecificationCreate]
