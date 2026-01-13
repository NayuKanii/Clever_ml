import die as dice_module

from categories import yellow
from categories import blue
from categories import green
from categories import orange
from categories import purple

SEPARATOR = "\n----------------------------------------\n"

dice = {"white": dice_module.Die(),
        "yellow": dice_module.Die(),
        "blue": dice_module.Die(),
        "green": dice_module.Die(),
        "orange": dice_module.Die(),
        "purple": dice_module.Die(),
        }

categories = {"yellow": yellow.Yellow(),
              "blue": blue.Blue(),
              "green": green.Green(),
              "orange": orange.Orange(),
              "purple": purple.Purple(),
              }


def roll_available_dice():
    print(f"{SEPARATOR}Rolled dice:\n")
    for key in dice:

        if dice[key].state == "platter":
            print(f"{key}: On silver platter")
            continue

        elif dice[key].state == "chosen":
            print(f"{key}: chosen")
            continue

        else:
            dice[key].roll()
            print(f"{key}: {dice[key].value}")

    print(SEPARATOR)


def get_choice():

    choice = ""
    input_string = (
        "Pick a die\n" +
        "or\n" +
        f"Use Reroll (enter r)\n{SEPARATOR}")

    while choice not in dice.keys() or not "r":
        choice = input(input_string)

    print("\n")
    return choice


def validate_choice(choice):

    if choice == 'r':
        # remove reroll
        return False

    elif dice[choice].state == "chosen":
        choice = get_choice()
        return validate_choice(choice)

    else:
        return True


def dice_roll_loop():

    roll_available_dice()
    choice = get_choice()

    if not validate_choice(choice):
        return dice_roll_loop()

    else:
        return choice


def update_dice_states(chosen_die):

    for key in dice:

        if dice[chosen_die] == dice[key]:
            dice[chosen_die].state = "chosen"
            continue

        else:
            if dice[chosen_die].value > dice[key].value:
                dice[key].state = "platter"


def Clever():

    for round_num in range(1, 7):
        for throw_num in range(1, 4):

            chosen_die = dice_roll_loop()
            update_dice_states(chosen_die)
            categories[chosen_die].fill_value(dice[chosen_die].value)


if __name__ == "__main__":
    Clever()
