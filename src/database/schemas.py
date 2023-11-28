from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    user_id: int = Field(ge=5*10**6, le=2*10**7)
    name: str = Field(min_length=3, encodings=['utf-8'])
    current_mn_page: int = Field(ge=0)
    answers: int = Field(ge=0)
    right_answers: int = Field(ge=0)
    wrong_answers: int = Field(ge=0)


class User:
    def __init__(self, user_id, name, current_mn_page=0, answers=0, right_answers=0, wrong_answers=0):
        self.user_id = user_id
        self.name = name
        self.current_mn_page = current_mn_page
        self.answers = answers
        self.right_answers = right_answers
        self.wrong_answers = wrong_answers


    def get_dict(self):
        return {k: v for k, v in self.__dict__.items()}


# us = User(5888888, "Alexandr", 123, 10, 50, 11)
#
# print(us.get_dict())