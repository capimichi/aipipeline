from typing import List, Dict, Any, Optional

from pydantic import BaseModel


class Task(BaseModel):
    id: str
    type: str
    inputs: Optional[Dict[str, Any]] = None
    outputs: Optional[Dict[str, Any]] = None
    multiple: Optional[bool] = False

    def get_inputs(self):
        return self.inputs or {}

    def get_outputs(self):
        return self.outputs or {}

    def is_multiple(self):
        return self.multiple
