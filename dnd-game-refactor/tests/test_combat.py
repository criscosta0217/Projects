from unittest.mock import patch

from dndgame.character import Character
from dndgame.combat import Combat
from dndgame.enemy import Enemy


def make_player() -> Character:
    player = Character("Hero", "Human", 10)
    player.stats = {
        "STR": 10,
        "DEX": 10,
        "CON": 10,
        "INT": 10,
        "WIS": 10,
        "CHA": 10,
    }
    player.hp = 10
    player.max_hp = 10
    player.armor_class = 10
    return player


def make_enemy() -> Enemy:
    enemy = Enemy("Goblin", 5)
    enemy.stats = {
        "STR": 10,
        "DEX": 10,
        "CON": 10,
        "INT": 8,
        "WIS": 8,
        "CHA": 8,
    }
    enemy.hp = 5
    enemy.max_hp = 5
    enemy.armor_class = 10
    return enemy


def test_combat_initializes_correctly() -> None:
    player = make_player()
    enemy = make_enemy()
    combat = Combat(player, enemy)

    assert combat.player is player
    assert combat.enemy is enemy
    assert combat.round == 1
    assert combat.initiative_order == []


@patch("dndgame.combat.roll")
def test_roll_initiative_returns_two_entities(mock_roll) -> None:
    player = make_player()
    enemy = make_enemy()
    mock_roll.side_effect = [15, 10]

    combat = Combat(player, enemy)
    order = combat.roll_initiative()

    assert len(order) == 2
    assert order[0] is player
    assert order[1] is enemy


@patch("dndgame.combat.roll")
def test_attack_returns_zero_on_miss(mock_roll) -> None:
    player = make_player()
    enemy = make_enemy()
    enemy.armor_class = 20
    mock_roll.return_value = 5

    combat = Combat(player, enemy)
    damage = combat.attack(player, enemy)

    assert damage == 0
    assert enemy.hp == 5


@patch("dndgame.combat.roll")
def test_attack_reduces_hp_on_hit(mock_roll) -> None:
    player = make_player()
    enemy = make_enemy()
    player.stats["STR"] = 14
    enemy.armor_class = 10
    mock_roll.side_effect = [15, 4]

    combat = Combat(player, enemy)
    damage = combat.attack(player, enemy)

    assert damage == 4
    assert enemy.hp == 1


def test_combat_is_over_when_enemy_has_zero_hp() -> None:
    player = make_player()
    enemy = make_enemy()
    enemy.hp = 0

    combat = Combat(player, enemy)

    assert combat.is_over() is True


def test_combat_is_over_when_player_has_zero_hp() -> None:
    player = make_player()
    enemy = make_enemy()
    player.hp = 0

    combat = Combat(player, enemy)

    assert combat.is_over() is True