'''
The orange category is a fill in category. Just fill in the value of the die
when picked and multiply if needed. Actions & bonuses are gained when a value
is filled in the field above it.
'''

orange_row = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0,
              11: 0}

orange_index = 1

orange_multipliers = {4: "x2", 7: "x2", 9: "x2", 11: "x3"}

orange_actions = {3: "reroll", 6: "extra_die"}

orange_bonuses = {5: "cross_yellow", 8: "fox", 10: "six_purple"}


class Orange():

    def __init__(self,
                 orange_row=orange_row,
                 orange_index=orange_index,
                 orange_multipliers=orange_multipliers,
                 orange_actions=orange_actions,
                 orange_bonuses=orange_bonuses,):

        self.row = orange_row
        self.index = orange_index
        self.multipliers = orange_multipliers
        self.actions = orange_actions
        self.bonuses = orange_bonuses

    def fill_value(self, value):

        if self.index not in self.multipliers.keys():

            self.row[self.index] = value
            self.index += 1

        else:
            if self.multipliers[self.index] == "x2":

                self.row[self.index] = value * 2
                self.index += 1

            elif self.multipliers[self.index] == "x3":

                self.row[self.index] = value * 3
                self.index += 1

    def points(self):

        total_points = sum(list(self.row.values()))
        return total_points
