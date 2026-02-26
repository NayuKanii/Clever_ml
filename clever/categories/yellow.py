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

yellow_column_points = [10, 14, 16, 20]

yellow_actions = ["extra_die"]

yellow_bonuses = ["cross_blue", "four_orange", "cross_green", "fox"]


class Yellow:

    def __init__(self,
                 grid=yellow_grid,
                 column_points=yellow_column_points,
                 actions=yellow_actions,
                 bonuses=yellow_bonuses):

        self.grid = grid
        self.column_points = column_points
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

    def make_grid(self):

        grid_2d = ""

        for row in self.grid:
            grid_2d += f"{row}\n"

        return grid_2d

    def enter_value(self, value, occurrence=0):
        """
        Enter a value at the specified occurrence.

        Args:
            value: the die value to enter
            occurrence: which occurrence of this value (0 or 1 for most values)
        """
        coordinates = self.coordinates(value)

        # Make sure the occurrence is valid
        if occurrence >= len(coordinates):
            raise ValueError(
                f"Occurrence {occurrence} is invalid for value {value}")

        row = coordinates[occurrence][0]
        column = coordinates[occurrence][1]
        self.grid[row][column] = 'x'

    def points(self):
        '''
        Calculate the current points for the yellow category
        '''
        total = 0

        # Check each column (0-3)
        for col in range(4):
            column_complete = True

            # Check if every cell in this column is crossed
            for row in range(4):
                if self.grid[row][col] != 'x':
                    column_complete = False
                    break

            # If column is complete, add its point value
            if column_complete:
                total += self.column_points[col]

        return total
