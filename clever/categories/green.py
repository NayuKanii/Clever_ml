'''
The green category progresses from left to right. Boxes are crossed by taking
the green or white die with a value equal or greater than the value in the box.
Points are gained based on the amount of boxes crossed. Actions and bonuses are
gained when you cross the box below which it is placed.
'''

green_row = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 1, 7: 2, 8: 3, 9: 4, 10: 5,
             11: 6}

green_index = 1

green_available_points = {1: 1, 2: 3, 3: 6, 4: 10, 5: 15, 6: 21, 7: 28, 8: 36,
                          9: 45, 10: 55, 11: 66}

green_actions = {4: "extra_die", 10: "reroll"}

green_bonuses = {6: "cross_blue", 7: "fox", 9: "six_purple"}


class Green:

    def __init__(self,
                 green_row=green_row,
                 green_index=green_index,
                 available_points=green_available_points,
                 actions=green_actions,
                 bonuses=green_bonuses):

        self.row = green_row
        self.index = green_index
        self.available_points = available_points
        self.actions = actions
        self.bonuses = bonuses

    def cross(self, value):

        if value >= self.row[green_index]:

            self.row[green_index] = 'x'
            self.index += 1

        else:
            return

    def points(self):

        return self.available_points[green_index]
