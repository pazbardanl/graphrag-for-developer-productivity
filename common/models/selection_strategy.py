from enum import Enum

class SelectionStrategy(Enum):
    UNDETERMINED = "undetermined"
    HEURISTIC = "heuristic"
    OPENAI = "openai"

    def from_string(value: str) -> 'SelectionStrategy':
        try:
            return SelectionStrategy(value.lower())
        except ValueError:
            return SelectionStrategy.UNDETERMINED