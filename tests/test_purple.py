from clever import purple

p1 = purple.Purple()


def test_fill_value():

    p1.fill_value(2)
    p1.fill_value(4)
    p1.fill_value(6)

    assert p1.row == {1: 2, 2: 4, 3: 6, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0,
                      10: 0, 11: 0}


def test_points():

    assert p1.points() == 12
