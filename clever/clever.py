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


def roll_dice():

    for key in dice:

        if dice[key].state == "platter":
            continue

        elif dice[key].state == "chosen":
            continue

        else:
            dice[key].roll()


def display_dice_values():

    print(SEPARATOR)

    for key in dice:
        if dice[key].state == "platter":
            print(f"{key} : On silver platter")
            continue

        elif dice[key].state == "chosen":
            print(f"{key} : chosen")
            continue

        else:
            print(f"{key} : {dice[key].value}")

    print(SEPARATOR)


def get_choice():

    input_string = ("Pick a die\n" + SEPARATOR)
    choice = input(input_string)

    print(SEPARATOR)

    return choice


def validate_choice(choice):

    if choice not in dice.keys():
        print("Please enter the dice name as displayed" + SEPARATOR)
        return validate_choice(get_choice)

    elif dice[choice].state == "On silver platter":
        print("Die is on platter" + SEPARATOR)
        return get_choice()

    elif dice[choice].state == "Chosen":
        print("Die alreay chosen" + SEPARATOR)
        return get_choice()

    else:
        return choice


def update_dice_states(chosen_die):

    for key in dice:

        if dice[chosen_die] == dice[key]:
            dice[chosen_die].state = "chosen"
            continue

        elif (dice[chosen_die].value > dice[key].value and
              dice[chosen_die].state != "chosen"):

            dice[key].state = "platter"


def reset_dice_states():

    for key in dice:
        dice[key].state = "hand"


def display_score():

    score = 0
    for category in categories.keys():
        score += categories[category].points()

    print(f"Total score: {score}")


def Clever():

    for round_number in range(1, 7):
        print(f"ROUND NUMBER : {round_number}")

        for throw_num in range(1, 4):
            print(f"THROW NUMBER : {throw_num}")

            roll_dice()
            display_dice_values()

            chosen_die = get_choice()
            chosen_die = validate_choice(chosen_die)
            update_dice_states(chosen_die)

            categories[chosen_die].fill_value(dice[chosen_die].value)

        reset_dice_states()

    display_score()


if __name__ == "__main__":
    Clever()
