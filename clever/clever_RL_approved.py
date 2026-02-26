import die as dice_module
from categories import yellow, blue, green, orange, purple

import copy


class CleverGame:
    '''
    Docstring for CleverGame
    '''

    def __init__(self):

        # Initialize dice
        self.dice = {
            "white": dice_module.Die(),
            "yellow": dice_module.Die(),
            "blue": dice_module.Die(),
            "green": dice_module.Die(),
            "orange": dice_module.Die(),
            "purple": dice_module.Die(),
            }

        # Initialize categories
        self.categories = {
            "yellow": yellow.Yellow(),
            "blue": blue.Blue(),
            "green": green.Green(),
            "orange": orange.Orange(),
            "purple": purple.Purple(),
            }

        # Variables for game state tracking
        self.current_round = 1
        self.current_throw = 1
        self.max_rounds = 6
        self.max_throws = 3

        # Variables for game phase
        self.phase = "NEED_ROLL"
        self.chosen_die_name = None
        self.chosen_value = None

    def reset(self):
        '''
        Reset game to initial state
        '''
        self.__init__()
        return self.get_state()

    def get_state(self):
        '''
        Return game state as dictionary
        '''
        return {
            "dice_values":
            {name: die.value for name, die in self.dice.items()},
            "dice_states":
            {name: die.state for name, die in self.dice.items()},

            "current_round": self.current_round,
            "current_throw": self.current_throw,

            "phase": self.phase,

            "yellow_grid": copy.deepcopy(self.categories["yellow"].grid),

            "blue_grid": copy.deepcopy(self.categories["blue"].grid),

            "green_row": copy.deepcopy(self.categories["green"].row),
            "green_index": self.categories["green"].index,

            "orange_row": copy.deepcopy(self.categories["orange"].row),
            "orange_index": self.categories["orange"].index,

            "purple_row": copy.deepcopy(self.categories["purple"].row),
            "purple_index": self.categories["purple"].index,
        }

    def get_legal_actions(self):
        '''
        Returns list of legal actions
        '''
        if self.phase == "NEED_ROLL":
            return [{"action_type": "roll"}]

        elif self.phase == "NEED_DIE_CHOICE":
            legal_dice = []

            for name, die in self.dice.items():
                if die.state == "hand":
                    # Check if this die can actually be placed
                    if self._can_place_die(name, die.value):
                        legal_dice.append({"action_type": "choose_die",
                                           "die_name": name})
            return legal_dice

        elif self.phase == "NEED_CATEGORY":
            # If the white die was chosen, a category needs to be specified
            # But only return categories where the value can actually be placed
            legal_categories = []
            white_value = self.dice["white"].value

            for cat in self.categories.keys():
                if self._can_place_in_category(cat, white_value):
                    legal_categories.append({"action_type": "need_category",
                                            "category": cat})

            # If no categories available, skip to next round
            if len(legal_categories) == 0:
                print("No valid categories, skipping to next round.")
                self._skip_to_next_round()
                return self.get_legal_actions()

            return legal_categories

        elif self.phase == "NEED_PLACEMENT":
            return self._get_enter_actions()

        return []

    def _can_place_die(self, die_name, die_value):
        '''
        Check if a die can be placed according to game rules.
        This prevents choosing dice that have no valid placement.
        '''
        if die_name == "white":
            # White can be used if ANY category can accept it
            for cat in self.categories.keys():
                if self._can_place_in_category(cat, die_value):
                    return True
            return False
        else:
            # For colored dice, check if it can be placed in its own category
            return self._can_place_in_category(die_name, die_value)

    def _can_place_in_category(self, category_name, value):
        '''
        Check if a value can be placed in a specific category.
        Returns True if there's at least one valid placement.
        '''
        if category_name == 'yellow':
            coords = self.categories['yellow'].coordinates(value)
            # Can place if there are any available coordinates
            return len(coords) > 0

        elif category_name == 'blue':
            # For blue, the value is blue + white
            blue_value = self.dice['blue'].value
            white_value = self.dice['white'].value
            total_value = blue_value + white_value
            coords = self.categories['blue'].coordinates(total_value)
            return coords is not None and len(coords) > 0

        elif category_name == 'green':
            current_required = (
                self.categories['green'].row[self.categories['green'].index])
            return value >= current_required

        elif category_name == 'orange':
            # Orange always accepts values (unless full)
            return self.categories['orange'].index <= 11

        elif category_name == 'purple':
            purple_index = self.categories['purple'].index

            # Purple full?
            if purple_index > 11:
                return False

            # First entry?
            if purple_index == 1:
                return True

            # Check if value is valid based on previous
            previous_value = self.categories['purple'].row[purple_index - 1]
            return previous_value == 6 or value > previous_value

        return False

    def _get_enter_actions(self):
        '''
        Adds the correct enter action to the agent's available action list,
        based on the chosen category
        '''
        actions = []

        if self.chosen_die_name == 'yellow':
            # Yellow: may have multiple occurrences of the same value
            coords = self.categories['yellow'].coordinates(self.chosen_value)
            for i, coord in enumerate(coords):
                actions.append({
                    'action_type': 'enter_yellow',
                    'occurrence': i
                })

        elif self.chosen_die_name == 'blue':
            # Blue: only one spot per value
            actions.append({'action_type': 'enter_blue'})

        elif self.chosen_die_name == 'green':
            # Green: automatic placement at current index
            actions.append({'action_type': 'enter_green'})

        elif self.chosen_die_name == 'orange':
            # Orange: automatic placement at current index
            actions.append({'action_type': 'enter_orange'})

        elif self.chosen_die_name == 'purple':
            # Purple: automatic placement at current index
            actions.append({'action_type': 'enter_purple'})

        return actions

    def step(self, action):
        '''
        Execute one action and advance game state

        args:
            action: dictionary with action info,
            e.g. {"action_type": "choose_die", "die_name": "yellow"}

        returns:
            state: the new game state
            reward: reward for this action
            done: whether the game is over
            info: additional info
        '''
        current_score = self.get_score()

        # Execute action based on phase
        if action["action_type"] == "roll":
            self._roll_dice()
            self.phase = "NEED_DIE_CHOICE"

        elif action["action_type"] == "choose_die":
            self._choose_die(action["die_name"])

        elif action["action_type"] == "need_category":
            self._assign_white_to_category(action["category"])

        # Entering values for each category
        elif action["action_type"] == "enter_yellow":
            self._enter_yellow(action["occurrence"])
            self._advance_turn()

        elif action["action_type"] == "enter_blue":
            self._enter_blue()
            self._advance_turn()

        elif action["action_type"] == "enter_green":
            self._enter_green()
            self._advance_turn()

        elif action["action_type"] == "enter_orange":
            self._enter_orange()
            self._advance_turn()

        elif action["action_type"] == "enter_purple":
            self._enter_purple()
            self._advance_turn()

        # Calculate reward
        new_score = self.get_score()
        reward = new_score - current_score

        # Check if game is done
        done = (self.phase == "GAME_OVER")

        # Return RL tuple for agent
        state = self.get_state()
        info = {
            "round": self.current_round,
            "throw": self.current_throw,
            "score": new_score
        }

        return state, reward, done, info

    def _enter_yellow(self, occurence):
        '''
        Cross off the value in the grid at the specified occurence
        '''
        coordinates = self.categories["yellow"].coordinates(self.chosen_value)
        row, col = coordinates[occurence]
        self.categories["yellow"].grid[row][col] = 'x'

    def _enter_blue(self):
        '''
        Cross off the value in the grid
        '''
        self.categories["blue"].enter_value(self.chosen_value)

    def _enter_green(self):
        '''
        Cross off the next box in the green row
        '''
        self.categories["green"].enter_value(self.chosen_value)

    def _enter_orange(self):
        '''
        Enter the value into the orange row
        '''
        self.categories["orange"].enter_value(self.chosen_value)

    def _enter_purple(self):
        '''
        Enter the value into the purple row
        '''
        self.categories["purple"].enter_value(self.chosen_value)

    def _roll_dice(self):
        '''
        Roll all dice that are in hand
        '''
        for die in self.dice.values():
            if die.state == "hand":
                die.roll()

    def _choose_die(self, die_name):
        '''
        Agent chooses a die
        '''
        self.chosen_die_name = die_name

        # Update dice states (smaller dice go to platter)
        chosen_value = self.dice[die_name].value
        for name, die in self.dice.items():
            if name == die_name:
                die.state = "chosen"
            elif die.value < chosen_value and die.state == "hand":
                die.state = "platter"

        # Check if white die was chosen
        if die_name == "white":
            self.phase = "NEED_CATEGORY"
        else:
            self._determine_value()
            self.phase = "NEED_PLACEMENT"  # We know placement is valid

    def _skip_to_next_round(self):
        """Skip remaining throws and move to next round"""
        self._reset_dice_states()
        self.current_throw = 1
        self.current_round += 1

        if self.current_round > self.max_rounds:
            self.phase = "GAME_OVER"

        else:
            self.phase = "NEED_ROLL"

    def _assign_white_to_category(self, category_name):
        '''
        Assign white die to a category
        '''
        self.chosen_die_name = category_name
        self._determine_value()
        self.phase = "NEED_PLACEMENT"

    def _determine_value(self):
        '''
        Determine the true value to be entered into a category
        '''
        if self.chosen_die_name == "blue":
            # Blue value is blue + white
            self.chosen_value = (self.dice["blue"].value +
                                 self.dice["white"].value)

        else:
            self.chosen_value = self.dice[self.chosen_die_name].value

    def _enter_value(self):
        '''
        Enter the value into it's category
        '''
        self.categories[self.chosen_die_name].enter_value(self.chosen_value)

    def _advance_turn(self):
        '''
        Move to next throw or round
        '''
        self.current_throw += 1

        if self.current_throw > self.max_throws:
            # round has ended
            self._reset_dice_states()
            self.current_throw = 1
            self.current_round += 1

            if self.current_round > self.max_rounds:
                self.phase = "GAME_OVER"
            else:
                self.phase = "NEED_ROLL"

        else:
            # Next throw in same round
            self.phase = "NEED_ROLL"

    def _reset_dice_states(self):
        '''
        Resets all the dice to hand
        '''
        for die in self.dice.values():
            die.state = "hand"

    def get_score(self):
        '''
        Calculate the current score
        '''
        total = 0
        for category in self.categories:
            total += self.categories[category].points()
        return total

    def is_game_over(self):
        '''
        Verify whether game has ended or not
        '''
        return self.phase == "GAME_OVER"


# Code for manual testing
def play_manual_game():
    '''Play game manually for testing'''
    game = CleverGame()

    while not game.is_game_over():
        state = game.get_state()
        legal_actions = game.get_legal_actions()

        print(f"\nRound {state["current_round"]},",
              f"Throw {state["current_throw"]}")
        print(f"Phase: {state["phase"]}")
        print(f"Dice: {state["dice_values"]}")

        print("\nLegal actions:")
        for i, action in enumerate(legal_actions):
            print(f"{i}: {action}")

        choice = int(input("Choose action number: "))
        action = legal_actions[choice]

        state, reward, done, info = game.step(action)
        print(f"Reward: {reward}, Score: {info["score"]}")

    print(f"\nGame Over! Final score: {game.get_total_score()}")


if __name__ == "__main__":
    play_manual_game()
