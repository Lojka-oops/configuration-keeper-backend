from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    """Base schema
    
    """

    id: int = Field(..., description="Entity identifier")
    created_at: datetime = Field(..., description="Create date")
    updated_at: datetime = Field(None, description="Update date")
    is_deleted: bool = Field(None, description="Delete indicator")
    deleted_at: datetime = Field(None, description="Delete date")
