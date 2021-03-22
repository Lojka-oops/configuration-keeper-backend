from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from schemas.variables_schemas import VariableSchema


class ConfigurationSchema(BaseModel):
    """Returns basic configuration data
    
    """

    environment_name: str = Field(..., description="Environment name")
    variables: List[VariableSchema] = Field(..., description="List of environment variables")
