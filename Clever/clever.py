import dice


def clever():

    for i, round_num in enumerate(6):

        for i, roll_num in enumerate(3):

            print(f"Round: {round_num}/nRoll: {roll_num}")
            dice.roll_dice()
