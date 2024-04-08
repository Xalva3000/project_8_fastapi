from pydantic import BaseModel, Field
from typing import Optional


class ExecutionForm(BaseModel):
    execution: Optional[int] = Field(default=None, gt=0)
    payment: Optional[int] = Field(default=None, gt=0)
    reserve: Optional[int] = Field(default=None, gt=0)
    delete: Optional[int] = Field(default=None, gt=0)

    def get_demand(self):
        for key, value in self.model_dump().items():
            if value:
                return key, value


form = ExecutionForm()

if form.model_dump(exclude_unset=True):
    print(form)
print(form.model_dump(exclude_unset=True))
