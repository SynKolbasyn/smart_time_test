from typing import Annotated, List

from pydantic import BaseModel, EmailStr, Field


class Register(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]


class Exam(BaseModel):
    subject_name: str
    room_number: int


class ExamsRegister(BaseModel):
    user_email: EmailStr
    exams: Annotated[List[Exam], Field(min_length=1)]
