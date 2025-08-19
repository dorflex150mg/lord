from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError, field_validator

from instance import Instance
from util import consts

class LoadBalancer(BaseModel):
    id: str = Field(..., min_length=1)
    name: str  = Field(..., min_length=1)
    ports: Optional[List[int]]
    instances: List[Instance] = []

    @field_validator("ports")
    def non_empty_ports(cls, ports: Optional[List[int]]) -> Optional[List[int]]: # pylint: disable=no-self-argument
        if ports is not None:
            if [item for item in ports if item <= 0 or item > consts.MAX_PORT]:
                raise ValidationError("Invalid port number added to Load Balancer {self.name}."
                                      "Port numbers must be between 0 and {consts.MAX_PORT}")
            return ports
