from dataclasses import dataclass
from abc import ABC

from API.NarutoCharacter import Character


@dataclass()
class CharacterInfo():
    Misc: str
    Stats: str
    Skills: str
    Abilities: str
    Jutsu: str
