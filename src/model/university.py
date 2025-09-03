from enum import Enum
from pydantic import BaseModel


class ModelName(str, Enum):
    midwestern = "MIDWESTERN"