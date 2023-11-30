from pydantic import BaseModel, EmailStr, ConfigDict


class Phone(BaseModel):
    phone_id: int
    contractor_id: int
    name: str
    phone: str


class Email(BaseModel):
    email_id: int
    contractor_id: int
    name: str
    email: EmailStr


class ContractorBase(BaseModel):
    # contractor_id: int
    name: str
    address: str


class ContractorCreate(ContractorBase):
    pass


class ContractorUpdate(ContractorBase):
    pass


class ContractorUpdatePartial(ContractorBase):
    # contractor_id: int | None = None
    name: str | None = None
    address: str | None = None


class Contractor(ContractorBase):
    model_config = ConfigDict(from_attributes=True)

    contractor_id: int
