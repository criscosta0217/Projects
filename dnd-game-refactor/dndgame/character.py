from dataclasses import dataclass, field
from dndgame.dice import roll
from dndgame.entity import Entity


RACIAL_BONUSES: dict[str, dict[str, int]] = {
    "Human": {"STR": 1, "DEX": 1, "CON": 1, "INT": 1, "WIS": 1, "CHA": 1},
    "Elf": {"DEX": 2},
    "Dwarf": {"CON": 2},
    "Orc": {"STR": 2},
}


@dataclass(init=False)
class Character(Entity):
    """Represents a player-controlled character in the game.

    A character has a name, race, ability scores (stats), hit points,
    and an armor class used during combat.

    Attributes:
        name: Character's name.
        race: Character's race (Human, Elf, Dwarf, etc.).
        base_hp: Base hit points before modifiers.
        stats: Dictionary storing ability scores.
        hp: Current hit points.
        max_hp: Maximum hit points.
        armor_class: Defensive value used during combat.
        level: Character level.
    """

    race: str = ""
    level: int = 1

    def __init__(self, name: str, race: str, base_hp: int) -> None:
        """Initialize a new character.

        Args:
            name: Name of the character.
            race: Selected character race.
            base_hp: Base hit points before modifiers.
        """
        super().__init__(name=name, base_hp=base_hp)
        self.race = race
        self.level = 1

    def roll_stats(self) -> None:
        """Roll random ability scores for the character.

        Each stat is rolled using the dice module and stored
        in the character's stats dictionary. Hit points are
        recalculated based on the Constitution modifier.
        """
        print("Rolling stats...\n")
        stats: list[str] = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]

        self.stats = {stat: roll(6, 3) for stat in stats}

        self.max_hp = self.base_hp + self.get_modifier("CON")
        self.hp = self.max_hp

    def apply_racial_bonuses(self) -> None:
        """Apply racial bonuses to the character's stats.

        Different races grant different stat bonuses.
        """
        bonuses = RACIAL_BONUSES.get(self.race, {})

        for stat, bonus in bonuses.items():
            self.stats[stat] += bonus

        self.max_hp = self.base_hp + self.get_modifier("CON")
        self.hp = self.max_hp