import pydantic
from pydantic import BaseModel
#
# dct = {'one': 1, 'two': 2, 'three': 3, 'four': 4}
#
#
# class Scheme(BaseModel):
#     one: int
#     two: int
#     three: int
#
#
# class SchemeFour(BaseModel):
#     four: int
#
#
# scheme3 = Scheme(**dct)
# scheme4 = SchemeFour(**dct)
# print(scheme3)
# print(scheme4)

from faker import Faker

fake = Faker("ru_RU")
print(*[fake.company() for _ in range(20)], sep='\n')
print(*[fake.address() for _ in range(20)], sep='\n')
