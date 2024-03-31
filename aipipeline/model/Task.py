from typing import List, Dict, Any, Optional

from pydantic import BaseModel


class Task(BaseModel):
    id: str
    type: str
    inputs: Optional[Dict[str, Any]] = None
    outputs: Optional[Dict[str, Any]] = None

    def get_inputs(self):
        return self.inputs or {}

    def get_outputs(self):
        return self.outputs or {}
