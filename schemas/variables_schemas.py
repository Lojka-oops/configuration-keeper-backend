from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class VariableBaseSchema(BaseModel):
    """Returns basic variable data
    
    """

    id: int = Field(..., description="Variable identifier")
    name: str = Field(..., description="Variable name")
    value: str = Field(..., description="Variable value")
    created_at: datetime = Field(..., description="Variable creation date")
    updated_at: Optional[datetime] = Field(None, description="Variable updation date")


class VariableCreateSchema(BaseModel):
    """Validates a request to create/update an variable

    """

    env_id: int = Field(..., description="Identifier of environment that owns this variable")
    name: str = Field(..., description="Variable name")
    value: str = Field(..., description="Variable value")


class VariableDetailsSchema(VariableBaseSchema):
    """Returns detail variable data
    
    """

    env_id: int = Field(..., description="Identifier of environment that owns this variable")
    is_deleted: bool = Field(..., description="Variable deletion indicator")
    deleted_at: datetime = Field(..., description="Variable deletion date")


class VariablesListSchema(BaseModel):
    """Returns list of variables with total count
    
    """

    total_count: int = Field(..., description="Total count of variables for environment")
    data: List[VariableBaseSchema] = Field(..., description="List of variables")
