from dndgame.character import Character


def test_character_initialization():
    character = Character("Hero", "Human", 10)

    assert character.name == "Hero"
    assert character.race == "Human"
    assert character.base_hp == 10
    assert character.level == 1
    assert character.armor_class == 10


def test_get_modifier():
    character = Character("Hero", "Human", 10)
    character.stats["STR"] = 14

    assert character.get_modifier("STR") == 2


def test_apply_racial_bonus_dwarf():
    character = Character("Hero", "Dwarf", 10)
    character.stats = {
        "STR": 10,
        "DEX": 10,
        "CON": 10,
        "INT": 10,
        "WIS": 10,
        "CHA": 10,
    }

    character.apply_racial_bonuses()

    assert character.stats["CON"] == 12


def test_apply_racial_bonus_elf():
    character = Character("Hero", "Elf", 10)
    character.stats = {
        "STR": 10,
        "DEX": 10,
        "CON": 10,
        "INT": 10,
        "WIS": 10,
        "CHA": 10,
    }

    character.apply_racial_bonuses()

    assert character.stats["DEX"] == 12


def test_apply_racial_bonus_human():
    character = Character("Hero", "Human", 10)
    character.stats = {
        "STR": 10,
        "DEX": 10,
        "CON": 10,
        "INT": 10,
        "WIS": 10,
        "CHA": 10,
    }

    character.apply_racial_bonuses()

    assert character.stats["STR"] == 11
    assert character.stats["DEX"] == 11
    assert character.stats["CON"] == 11

def test_apply_racial_bonus_orc():
    character = Character("Hero", "Orc", 10)
    character.stats = {
        "STR": 10,
        "DEX": 10,
        "CON": 10,
        "INT": 10,
        "WIS": 10,
        "CHA": 10,
    }

    character.apply_racial_bonuses()

    assert character.stats["STR"] == 12


def test_dwarf_racial_bonus_updates_hit_points():
    character = Character("Hero", "Dwarf", 10)
    character.stats = {
        "STR": 10,
        "DEX": 10,
        "CON": 10,
        "INT": 10,
        "WIS": 10,
        "CHA": 10,
    }

    character.apply_racial_bonuses()

    assert character.max_hp == 11
    assert character.hp == 11