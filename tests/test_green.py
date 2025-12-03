from clever.categories import green

g1 = green.Green()


def test_cross():

    g1.cross(1)
    assert g1.index == 2, g1.row == {1: 'x', 2: 2, 3: 3, 4: 4, 5: 5, 6: 1,
                                     7: 2, 8: 3, 9: 4, 10: 5, 11: 6}


def test_points():

    assert g1.points() == 1
