from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated
from annotated_types import MinLen


class CreateProducer(BaseModel):
    # name: str = Field(..., min_length=3)
    name: Annotated[str, MinLen(3)]
    address: Optional[str] = None
    phone: Optional[str] = None
    email: EmailStr

