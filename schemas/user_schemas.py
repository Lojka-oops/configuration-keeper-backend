from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, EmailStr

from .base_schemas import BaseSchema


class UserSchema(BaseSchema):
    """Returns user data
    
    """

    name: str = Field(..., description="User name")
    email: EmailStr = Field(..., description="User email")


class UserCreateUpdateSchema(BaseModel):
    """Validates a request to create/update an user

    """

    name: str = Field(..., description="User name")
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="User password")



