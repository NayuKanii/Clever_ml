from clever.categories import blue

b1 = blue.Blue()


def test_coordinates():

    assert b1.coordinates(3) == [0, 2]
    assert b1.coordinates(12) == [2, 3]


def test_cross():

    b1.cross(6)
    assert b1.grid == [['', 2, 3, 4],
                       [5, 'x', 7, 8,],
                       [9, 10, 11, 12]]


def test_points():

    b1.cross(2)
    b1.cross(3)
    assert b1.points() == 4
