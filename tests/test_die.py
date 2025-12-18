from clever import die

white_die = die.Die()


def test_roll():

    white_die.roll()
    assert white_die.value >= 1 and white_die.value <= 6


def test_update_state_to_platter():

    white_die.update_state("platter")
    assert white_die.state == "platter"


def test_update_state_to_hand():

    white_die.update_state("hand")
    assert white_die.state == "hand"


def test_update_state_to_chosen():

    white_die.update_state("chosen")
    assert white_die.state == "chosen"
