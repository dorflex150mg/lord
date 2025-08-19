"""
Module containing the LoadBalancer BaseModel
"""
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError, field_validator

from instance import Instance
from util import consts

class LoadBalancer(BaseModel): #pylint: disable=too-few-public-methods

    """
    This class represents a Load Balancer, responsible for distributing traffic
    among the Instances of a Service.
    Attributes:
        id (str): the unique id that identifies this load balancer.
        name (str): the human-readable name of this load balancer.
        ports (Optional[List[int]]): the ports this load balancer serves on the 
        instances.
        instances: The instances served by this load balancer.
    """
    id: str = Field(..., min_length=1)
    name: str  = Field(..., min_length=1)
    ports: Optional[List[int]]
    instances: List[Instance] = []

    @field_validator("ports")
    def non_empty_ports(cls, ports: Optional[List[int]]) -> Optional[List[int]]: # pylint: disable=no-self-argument
        """
        field validator for ports that ensures that they are within the valid port range.
        """
        if ports is not None:
            if [item for item in ports if item <= 0 or item > consts.MAX_PORT]:
                raise ValidationError("Invalid port number added to Load Balancer {self.name}."
                                      "Port numbers must be between 0 and {consts.MAX_PORT}")
        return ports
