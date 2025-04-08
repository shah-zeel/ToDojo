from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class Status(Enum):
    TODO = 1
    INPROGRESS = 2
    DONE = 3


@dataclass
class Todo:
    """Class to represent todos"""

    id: int
    description: str
    status: Status
    createdAt: datetime
    updatedAt: datetime

    def __str__(self):
        return f"{self.id} - {self.description} - {self.status} - {self.createdAt} - {self.updatedAt}"
