from pydantic import BaseModel, Field

class Instance(BaseModel):
    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    node_id: str = Field(..., min_length=1)
