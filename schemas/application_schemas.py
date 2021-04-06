from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from .base_schemas import BaseSchema


class ApplicationSchema(BaseSchema):
    """Returns application data
    
    """

    name: str = Field(..., description="Application name")
    description: str = Field(None, description="Application description")


class ApplicationCreateSchema(BaseModel):
    """Validates a request to create/update an application

    """

    name: str = Field(..., description="Application identifier")
    description: Optional[str] = Field(None, description="Application description")


class ApplicationsListSchema(BaseModel):
    """Returns list of applications with total count
    
    """

    total_count: int = Field(..., description="Total count of applications")
    data: List[ApplicationSchema] = Field(..., description="List of applications")
