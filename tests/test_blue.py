from clever.categories import blue

b1 = blue.Blue()


def test_coordinates():

    assert b1.coordinates(3) == [0, 2]
    assert b1.coordinates(12) == [2, 3]


def fill_value():

    b1.fill_value(6)
    assert b1.grid == [['', 2, 3, 4],
                       [5, 'x', 7, 8,],
                       [9, 10, 11, 12]]


def test_points():

    b1.fill_value(2)
    b1.fill_value(3)
    assert b1.points() == 2
