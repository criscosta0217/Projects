from dndgame.character import Character
from dndgame.dice import roll
from dndgame.enemy import Enemy
from dndgame.entity import Entity


class Combat:
    """Handles combat between a player and an enemy."""

    def __init__(self, player: Character, enemy: Enemy) -> None:
        """Initialize a combat encounter.

        Args:
            player: The player character.
            enemy: The enemy combatant.
        """
        self.player: Character = player
        self.enemy: Enemy = enemy
        self.round: int = 1
        self.initiative_order: list[Entity] = []

    def roll_initiative(self) -> list[Entity]:
        """Determine combat order based on initiative rolls.

        Returns:
            A list of entities ordered by initiative.
        """
        player_init = roll(20, 1) + self.player.get_modifier("DEX")
        enemy_init = roll(20, 1) + self.enemy.get_modifier("DEX")

        if player_init >= enemy_init:
            self.initiative_order = [self.player, self.enemy]
        else:
            self.initiative_order = [self.enemy, self.player]

        return self.initiative_order

    def attack(self, attacker: Entity, defender: Entity) -> int:
        """Resolve an attack from one entity to another.

        Args:
            attacker: The attacking entity.
            defender: The defending entity.

        Returns:
            The damage dealt. Returns 0 if the attack misses.
        """
        attack_roll = roll(20, 1) + attacker.get_modifier("STR")

        if attack_roll >= defender.armor_class:
            damage = roll(6, 1)
            defender.take_damage(damage)
            return damage

        return 0

    def is_over(self) -> bool:
        """Return whether combat has ended."""
        return not self.player.is_alive() or not self.enemy.is_alive()