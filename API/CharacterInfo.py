from dataclasses import dataclass
from abc import ABC

from API.NarutoCharacter import Character


@dataclass()
class CharacterInfo(Character, ABC):
    Misc: str
    Stats: str
    Skills: str
    Sync: str
    Abilities: str
    Jutsu: str
