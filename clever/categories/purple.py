'''
The purple category is similar to the purple category. The difference being
that now each next number has to be larger than the previous. The exception
being 6, filling in a 6 allows you to start from one again (or any other
number). Points are based on the values filled in each box. Actions and bonuses
are gained as you fill in the box above it.
'''

purple_row = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0,
              11: 0}

purple_index = 1

purple_actions = {3: "reroll", 5: "extra_die", 8: "reroll", 11: "extra_die"}

purple_bonuses = {4: "cross_blue", 6: "cross_yellow", 7: "fox",
                  9: "cross_green", 10: "six_purple"}


class Purple():

    def __init__(self,
                 purple_row=purple_row,
                 purple_index=purple_index,
                 purple_actions=purple_actions,
                 purple_bonuses=purple_bonuses,):

        self.row = purple_row
        self.index = purple_index
        self.actions = purple_actions
        self.bonuses = purple_bonuses

    def enter_value(self, value):

        self.row[self.index] = value
        self.index += 1

    def points(self):

        total_points = sum(list(self.row.values()))
        return total_points
