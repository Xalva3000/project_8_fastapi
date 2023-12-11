from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    fish: str
    cutting: str
    size: str | None
    producer: str
    package: str
    weight: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductUpdatePartial(ProductBase):
    fish: str | None = None
    cutting: str | None = None
    size: str | None = None
    producer: str | None = None
    package: str | None = None
    weight: int | None = None


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
