'''
Clever is played with six dice, one for each category and a white die that acts
as a "joker" die. The category dice can only filled in their matching category
and the white die can be used everywhere.
'''

import random


class Die():

    def __init__(self):

        self.value = 0
        self.state = "hand"
        self.distance_to_platter = 0

    def roll(self):

        self.value = random.randint(1, 6)
        return self.value

    def update_state(self, change):

        if change == "hand":
            self.state = "hand"

        elif change == "platter":
            self.state = "platter"

        elif change == "chosen":
            self.state = "chosen"

        else:
            print("Invalid change")
            return
