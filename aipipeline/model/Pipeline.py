from typing import List

from pydantic import BaseModel

from aipipeline.model.Task import Task


class Pipeline(BaseModel):

    tasks: List[Task]