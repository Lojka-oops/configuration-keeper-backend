from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class ApplicationBaseSchema(BaseModel):
    """Returns basic application data
    
    """

    id: int = Field(..., description="Application identifier")
    name: str = Field(..., description="Application name")
    description: Optional[str] = Field(None, description="Application description")
    created_at: datetime = Field(..., description="Application creation date")
    updated_at: Optional[datetime] = Field(None, description="Application updation date")


class ApplicationCreateSchema(BaseModel):
    """Validates a request to create/update an application

    """

    name: str = Field(..., description="Application identifier")
    description: Optional[str] = Field(None, description="Application description")


class ApplicationDetailsSchema(ApplicationBaseSchema):
    """Returns detail application data
    
    """

    is_deleted: bool = Field(..., description="Application deletion indicator")
    deleted_at: datetime = Field(..., description="Application deletion date")


class ApplicationsListSchema(BaseModel):
    """Returns list of applications with total count
    
    """

    total_count: int = Field(..., description="Total count of applications")
    data: List[ApplicationBaseSchema] = Field(..., description="List of applications")
