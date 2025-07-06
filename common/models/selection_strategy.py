from enum import Enum

class SelectionStrategy(Enum):
    UNDETERMINED = "undetermined"
    HEURISTIC = "heuristic"
    OPENAI = "openai"