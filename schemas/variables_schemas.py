from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from .base_schema import BaseSchema


class VariableSchema(BaseSchema):
    """Returns variable data
    
    """

    name: str = Field(..., description="Variable name")
    value: str = Field(..., description="Variable value")


class VariableCreateSchema(BaseModel):
    """Validates a request to create/update an variable

    """

    env_id: int = Field(..., description="Identifier of environment that owns this variable")
    name: str = Field(..., description="Variable name")
    value: str = Field(..., description="Variable value")


class VariablesListSchema(BaseModel):
    """Returns list of variables with total count
    
    """

    total_count: int = Field(..., description="Total count of variables for environment")
    data: List[VariableSchema] = Field(..., description="List of variables")
