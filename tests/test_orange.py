from clever.categories import orange

o1 = orange.Orange()


def test_fill_value():

    o1.fill_value(3)
    assert o1.row == {1: 3, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0,
                      10: 0, 11: 0}


def test_points():

    o1.fill_value(6)
    o1.fill_value(6)
    assert o1.points() == 15


def test_multipliers():

    o1.fill_value(5)
    assert o1.row[4] == 10
