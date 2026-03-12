from dataclasses import dataclass
from dndgame.entity import Entity


@dataclass
class Enemy(Entity):
    """Represents an enemy combatant."""