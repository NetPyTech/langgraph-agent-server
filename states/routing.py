from typing_extensions import TypedDict
from dataclasses import dataclass

@dataclass(kw_only=True)
class Routing(TypedDict):
    next: str = None
    previous: str = None