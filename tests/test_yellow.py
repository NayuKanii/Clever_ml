from clever.categories import yellow

y1 = yellow.Yellow()


def test_coordinates():

    assert y1.coordinates(3) == [[0, 0], [3, 1]]


def test_fill_value():

    y1.fill_value(6)
    assert y1.grid == [
                    [3, 'x', 5, 'x'],
                    [2, 1, 'x', 5],
                    [1, 'x', 2, 4],
                    ['x', 3, 4, 6],
                    ]
