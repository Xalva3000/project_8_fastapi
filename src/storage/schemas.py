from pydantic import BaseModel


class StorageBase(BaseModel):
    product_id: int
    quantity: int


class StorageCreate(StorageBase):
    pass


class StorageUpdate(StorageBase):
    pass


class StorageUpdatePartial(StorageBase):
    product_id: int | None = None
    quantity: int | None = None


class Storage(StorageBase):
    pass
