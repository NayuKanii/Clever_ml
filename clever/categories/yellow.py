'''
The yellow category is a 4x4 grid. Points are gained by crossing columns,
Bonuses are gained by crossing rows, and via the diagonal from top left to
bottom right. 4 boxes are already crossed. A box may be crossed when you match
the number.
'''


yellow_grid = [
    [3, 6, 5, 'x'],
    [2, 1, 'x', 5],
    [1, 'x', 2, 4],
    ['x', 3, 4, 6],
    ]

yellow_points = [10, 14, 16, 20]

yellow_actions = ["extra_die"]

yellow_bonuses = ["cross_blue", "four_orange", "cross_green", "fox"]


class Yellow:

    def __init__(self,
                 grid=yellow_grid,
                 points=yellow_points,
                 actions=yellow_actions,
                 bonuses=yellow_bonuses):

        self.grid = grid
        self.points = points
        self.actions = actions
        self.bonuses = bonuses
        pass

    def coordinates(self, value):

        coordinates = []

        for row, val in enumerate(self.grid):
            for col, val in enumerate(self.grid[row]):

                if val == value:
                    coordinates.append([row, col])

        return coordinates

    def cross(self, value, occurrence):

        coordinates = self.coordinates(value)
        row = coordinates[occurrence][0]
        column = coordinates[occurrence][1]
        self.grid[row][column] = 'x'
