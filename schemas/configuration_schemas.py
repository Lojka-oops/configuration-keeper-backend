from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from schemas.variable_schemas import VariableSchema


class ConfigurationSchema(BaseModel):
    """Returns configuration data
    
    """

    environment_name: str = Field(..., description="Environment name")
    variables: List[VariableSchema] = Field(..., description="List of environment variables")
