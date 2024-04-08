from datetime import datetime, date
from typing import Optional

from fastapi_filter import FilterDepends
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field

from src.database.models import Contract, Specification


class SpecificationFilter(Filter):
    product_id: Optional[int] = None

    class Constants(Filter.Constants):
        model = Specification


class ContractFilter(Filter):
    contract_type: Optional[str] = None
    contract_id: Optional[int] = None
    contractor_id: Optional[int] = None
    planned_date: Optional[date] = None
    product_id: Optional[SpecificationFilter] = FilterDepends(SpecificationFilter)

    # executed_at: Optional[datetime] = None
    # deleted_at__isnull: Optional[bool] = None

    class Constants(Filter.Constants):
        model = Contract


class PageForm(BaseModel):
    # current_page: int = Field(gt=0, default=1)
    # next_page: int = Field(gt=0, default=1)
    page: int = Field(gt=0, default=1)
    size: int = Field(gt=0, default=20)


# class PageForm:
#     REQUIRED_ATTRS = ('page', 'size')
#
#     def __init__(self, **kwargs):
#         for name, value in kwargs.items():
#             if name in self.REQUIRED_ATTRS and value.isdigit():
#                 self.__dict__[name] = int(value)


class ContractForm:
    REQUIRED_ATTRS = ('product_id', 'contract_id', 'contractor_id', 'planned_date', 'contract_type')

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            if name in self.REQUIRED_ATTRS:
                if name == 'product_id' and value.isdigit():
                    self.__dict__[name] = SpecificationFilter(product_id=int(value))
                elif name == 'planned_date' and value:
                    self.__dict__[name] = datetime.strptime(value, '%Y-%m-%d')
                elif name == 'contract_type' and value in ('income', 'outcome'):
                    self.__dict__[name] = value
                elif value.isdigit():
                    self.__dict__[name] = int(value)
