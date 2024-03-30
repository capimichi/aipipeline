from typing import List, Dict, Any, Optional

from pydantic import BaseModel


class Task(BaseModel):
    id: str
    type: str
    inputs: Optional[Dict[str, Any]] = None
    outputs: Optional[Dict[str, Any]] = None
