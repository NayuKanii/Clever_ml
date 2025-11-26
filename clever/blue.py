'''
The blue category is a 3x4 grid (with the first value missing), where boxes are
crossed off by picking the blue or white die. The box you cross is determined
by the sum of the blue and white die. Points are gained based on the number of
boxes crossed off. Actions and bonuses are obtained by crossing full columns
and rows.
'''

grid = [['', 2, 3, 4],
        [5, 6, 7, 8,],
        [9, 10, 11, 12]]

available_points = {1: 1, 2: 2, 3: 4, 4: 7, 5: 11, 6: 16,
                    7: 22, 8: 29, 9: 37, 10: 36, 11: 35}

actions = ["reroll", "extra_die"]

bonuses = ["five_orange", "cross_yellow", "fox", "cross_green", "six_purple"]


class Blue:

    def __init__(self, grid=grid, available_points=available_points,
                 actions=actions, bonuses=bonuses):

        self.grid = grid
        self.available_points = available_points
        self.actions = actions
        self.bonuses = bonuses

    def coordinates(self, value):

        coordinates = []

        for row, val in enumerate(self.grid):
            for col, val in enumerate(self.grid[row]):

                if val == value:
                    coordinates = [row, col]

        return coordinates

    def cross(self, value):

        coordinates = self.coordinates(value)
        row = coordinates[0]
        column = coordinates[1]
        self.grid[row][column] = 'x'

    def points(self):

        boxes_crossed = 0

        for row, val in enumerate(self.grid):
            for column, val in enumerate(self.grid[row]):

                if self.grid[row][column] == 'x':
                    boxes_crossed += 1

        return self.available_points[boxes_crossed]
