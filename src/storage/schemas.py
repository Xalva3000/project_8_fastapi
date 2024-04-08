from pydantic import BaseModel


class StorageItemBase(BaseModel):
    product_id: int
    available: int = 0
    owned: int = 0
    stored: int = 0


class StorageItemCreate(StorageItemBase):
    pass


class StorageItemUpdate(StorageItemBase):
    pass


class StorageItemUpdatePartial(StorageItemBase):
    product_id: int | None = None
    available: int | None = None
    owned: int | None = None
    stored: int | None = None


class StorageItem(StorageItemBase):
    pass
