"""
Module containing the Instance BaseModel.
"""
from pydantic import BaseModel, Field

class Instance(BaseModel):
    """
    This class represents an application instance. 
    Attributes:
        id (str): the unique id of this application instance.
        name (str): the human-readable name of this application instance.
        node_id: the node to which this application instance is scheduled.
    """
    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    node_id: str
