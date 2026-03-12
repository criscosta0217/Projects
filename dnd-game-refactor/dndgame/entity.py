from dataclasses import dataclass, field


@dataclass
class Entity:
    """Base class for anything that can participate in combat.

    Attributes:
        name: The entity's name.
        base_hp: Base hit points before modifiers.
        stats: Dictionary storing ability scores.
        hp: Current hit points.
        max_hp: Maximum hit points.
        armor_class: Defensive value used during combat.
    """

    name: str
    base_hp: int

    stats: dict[str, int] = field(default_factory=dict)
    hp: int = 0
    max_hp: int = 0
    armor_class: int = 10

    def get_modifier(self, stat: str) -> int:
        """Calculate the ability modifier for a stat.

        Args:
            stat: The ability score key.

        Returns:
            The calculated modifier.
        """
        return (self.stats[stat] - 10) // 2

    def is_alive(self) -> bool:
        """Return whether the entity is still alive."""
        return self.hp > 0

    def take_damage(self, damage: int) -> None:
        """Reduce hit points without going below zero.

        Args:
            damage: Amount of damage to apply.
        """
        self.hp = max(0, self.hp - damage)