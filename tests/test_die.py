from clever import dice

white_die = dice.Die()


def test_roll():

    white_die.roll()
    assert white_die.value >= 1 and white_die.value <= 6


def test_update_state():

    white_die.update_state("platter")
    assert white_die.on_platter is True
