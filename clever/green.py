'''
The green category progresses from left to right. Boxes are crossed by taking
the green or white die with a value equal or greater than the value in the box.
Points are gained based on the amount of boxes crossed. Actions and bonuses are
gained when you cross the box below which it is placed.
'''

green_row = []

available_points = {1: 1, 2: 3, 3: 6, 4: 10, 5: 15, 6: 21, 7: 28, 8: 36, 9: 45,
                    10: 55, 11: 66}

green_actions = {4: "extra_die", 10: "reroll"}

green_bonuses = {6: "cross_blue", 7: "fox", 9: "six_purple"}
