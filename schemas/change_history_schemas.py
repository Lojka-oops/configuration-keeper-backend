from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from schemas.variable_schemas import VariableSchema


class ChangeHistorySchema(BaseModel):
    """Returns change history data
    
    """

    id: int = Field(..., description="Entity identifier")
    entity_type: str = Field(..., description="Type of updating entity")
    entity_id: int = Field(..., description="Identifier of updating entity")
    field: str = Field(..., description="Updating field")
    old_value: str = Field(..., description="Old value of updating field")
    new_value: str = Field(..., description="New value of updating field")
    created_at: datetime = Field(..., description="Create date")


class ChangeHistoryListSchema(BaseModel):
    """Returns list of change history entities with total count
    
    """

    total_count: int = Field(..., description="Total count of change history entities")
    data: List[ChangeHistorySchema] = Field(..., description="List of change history entities")
