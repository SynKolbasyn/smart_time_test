from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class Register(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]
