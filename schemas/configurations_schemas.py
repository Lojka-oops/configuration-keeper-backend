from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from schemas.variables_schemas import VariableBaseSchema


class ConfigurationSchema(BaseModel):
    """Returns basic configuration data
    
    """

    environment_name: str = Field(..., description="Environment name")
    variables: List[VariableBaseSchema] = Field(..., description="List of environment variables")
