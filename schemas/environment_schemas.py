from datetime import datetime
from typing import Optional, List

from pydantic import UUID4, BaseModel, validator, Field

from .base_schemas import BaseSchema


class EnvironmentSchema(BaseSchema):
    """Returns environment data
    
    """

    name: str = Field(..., description="Environment name")
    code: UUID4 = Field(..., description="Environment unique code")
    description: str = Field(None, description="Environment description")

    @validator("code")
    def hexlify_token(cls, value):
        """Convert UUID to pure hex string

        """

        return value.hex


class EnvironmentCreateSchema(BaseModel):
    """Validates a request to create/update an environment

    """

    name: str = Field(..., description="Environment name")
    app_id: int = Field(..., description="Identifier of application that owns this environment")
    description: Optional[str] = Field(None, description="Environment description")


class EnvironmentsListSchema(BaseModel):
    """Returns list of environments with total count
    
    """

    total_count: int = Field(..., description="Total count of environments for application")
    data: List[EnvironmentSchema] = Field(..., description="List of environments")
