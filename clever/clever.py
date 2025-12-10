import dice as dice_module

from categories import yellow
from categories import blue
from categories import green
from categories import orange
from categories import purple

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

    for key in dice:

        if dice[key].on_platter:
            print(f"{key}: On silver platter")
            continue

        else:
            dice[key].roll()
            print(f"{key}: {dice[key].value}")

    print("\n")


def get_choice():

    choice = ""
    input_string = "Pick a die\n" + "or\n" + "Use Reroll (enter r)\n"

    while choice not in dice.keys() or not "r":
        choice = input(input_string)

    print("\n")
    return choice


def validate_choice(choice):

    if choice == 'r':
        # remove reroll
        return False

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
            continue

        else:
            if dice[chosen_die].value > dice[key].value:
                dice[key].on_platter = True


def Clever():

    for round_num in range(1, 7):

        player_state = "active"

        for throw_num in range(1, 4):

            chosen_die = dice_roll_loop()
            update_dice_states(chosen_die)
            categories[chosen_die].fill_value(dice[chosen_die].value)
            # BLUE IS NOT WORKING PROPERLY


if __name__ == "__main__":
    Clever()
