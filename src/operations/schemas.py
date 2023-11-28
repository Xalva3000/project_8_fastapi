from pydantic import BaseModel
from datetime import datetime


class OperationCreate(BaseModel):
    id: int
    quantity: str
    figi: str
    instrument_tupe: str
    data: datetime
    type: str
