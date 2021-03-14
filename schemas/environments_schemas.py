from datetime import datetime
from typing import Optional, List

from pydantic import UUID4, BaseModel, validator, Field


class EnvironmentBaseSchema(BaseModel):
    """Returns basic environment data
    
    """

    id: int = Field(..., description="Environment identifier")
    name: str = Field(..., description="Environment name")
    code: UUID4 = Field(..., description="Environment unique code")
    description: Optional[str] = Field(None, description="Environment description")
    created_at: datetime = Field(..., description="Environment creation date")
    updated_at: Optional[datetime] = Field(None, description="Environment updation date")

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


class EnvironmentDetailsSchema(EnvironmentBaseSchema):
    """Returns detail environment data
    
    """

    app_id: int = Field(..., description="Identifier of application that owns this environment")
    is_deleted: bool = Field(..., description="Environment deletion indicator")
    deleted_at: datetime = Field(..., description="Environment deletion date")


class EnvironmentsListSchema(BaseModel):
    """Returns list of environments with total count
    
    """

    total_count: int = Field(..., description="Total count of environments for application")
    data: List[EnvironmentBaseSchema] = Field(..., description="List of environments")
