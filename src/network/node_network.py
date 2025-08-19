from typing import Optional
from pydantic import BaseModel

class NodeNetwork(BaseModel):
    ipv4: Optional[str]
    ipv6: Optional[str]
