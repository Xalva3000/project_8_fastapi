from datetime import date

from pydantic import BaseModel, ConfigDict


class PossessionBase(BaseModel):
    product_id: int
    quantity: int


class PossessionCreate(PossessionBase):
    pass


class PossessionUpdate(PossessionBase):
    pass


class PossessionUpdatePartial(PossessionBase):
    product_id: int | None = None
    quantity: int | None = None


class Possession(PossessionBase):
    model_config = ConfigDict(from_attributes=True)
    # possession_id: int
