from dndgame.character import Character
from dndgame.combat import Combat
from dndgame.enemy import Enemy



def create_character():
    print("Welcome to D&D Adventure!")
    name = input("Enter your character's name: ")

    print("\nChoose your race:")
    print("1. Human (+1 to all stats)")
    print("2. Elf (+2 DEX)")
    print("3. Dwarf (+2 CON)")
    print("4. Orc (+2 STR)")

    while True:
        race_choice = input("Enter choice (1-4): ")

        if race_choice.isdigit() and 1 <= int(race_choice) <= 4:
            break

        print("Invalid choice. Please enter a number between 1 and 4.")

    race = ["Human", "Elf", "Dwarf", "Orc"][int(race_choice) - 1]

    character = Character(name, race, 10)
    character.roll_stats()
    character.apply_racial_bonuses()
    return character


def display_character(character):
    print(f"\n{character.name} the {character.race}")
    print("\nStats:")

    def format_stat(item):
        stat, value = item
        modifier = character.get_modifier(stat)
        sign = "+" if modifier >= 0 else ""
        return f"{stat}: {value} ({sign}{modifier})"

    stat_lines = list(map(format_stat, character.stats.items()))
    print("\n".join(stat_lines))

    print(f"\nHP: {character.hp}")


def simple_combat(player):
    print("\nA goblin appears!")

    goblin = Enemy("Goblin", 5)
    goblin.stats = {
        "STR": 10,
        "DEX": 10,
        "CON": 10,
        "INT": 8,
        "WIS": 8,
        "CHA": 8,
    }
    goblin.hp = 5
    goblin.max_hp = 5
    goblin.armor_class = 10

    combat = Combat(player, goblin)

    while not combat.is_over():
        print(f"\nGoblin HP: {goblin.hp}")
        print(f"{player.name} HP: {player.hp}")
        print("\nYour turn!")
        print("1. Attack")
        print("2. Run away")
        print()

        while True:
            choice = input("What do you do? ")

            if choice in {"1", "2"}:
                break

            print("Invalid choice. Please enter 1 or 2.")

        if choice == "1":
            damage = combat.attack(player, goblin)
            if damage > 0:
                print(f"You hit for {damage} damage!")
            else:
                print("You missed!")

            if goblin.is_alive():
                enemy_damage = combat.attack(goblin, player)
                if enemy_damage > 0:
                    print(f"The goblin hits you for {enemy_damage} damage!")
                else:
                    print("The goblin missed!")

        elif choice == "2":
            return False

    return player.is_alive()


def main():
    player = create_character()

    while True:
        print("\nWhat would you like to do?")
        print("1. Fight a goblin")
        print("2. View character")
        print("3. Quit")

        while True:
            choice = input("Enter choice (1-3): ")

            if choice in {"1", "2", "3"}:
                break

            print("Invalid choice. Please enter 1, 2, or 3.")

        if choice == "1":
            victory = simple_combat(player)
            if victory:
                print("You defeated the goblin!")
            else:
                if player.hp == 0:
                    print("You were defeated by the goblin!")
                else:
                    print("You ran away!")
        elif choice == "2":
            display_character(player)
        elif choice == "3":
            break


if __name__ == "__main__":
    main()