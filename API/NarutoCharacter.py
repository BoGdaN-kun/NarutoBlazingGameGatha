from dataclasses import dataclass
from abc import ABC


@dataclass()
class Character(ABC):
    Index: int
    Picture: str
    Name: str
    Rarity: str
    Element: str
    Type: str
    CharacterURL: str

