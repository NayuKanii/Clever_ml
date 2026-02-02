import numpy as np
from typing import Tuple, List, Dict
from clever_RL_approved import CleverGame


class CleverEnv:
    '''
    Reinforcement learning wrapper for the game.
    Converts game state to observations and actions to integers.
    '''

    def __init__(self):

        self.game = CleverGame()
        self._build_action_mapping()

    def _build_action_mapping(self):

        '''
        Create mapping between action integers and game actions.
        As the action space is fixed, this only needs to be done once.
        '''
        self.action_to_game = {}
        action_index = 0

        # Roll action
        self.action_to_game[action_index] = {"action_type": "roll"}
        action_index += 1

        # Choose die actions
        for die_name in ["white", "yellow", "blue",
                         "green", "orange", "purple"]:

            action = {"action_type": "choose_die", "die_name": die_name}
            self.action_to_game[action_index] = action
            action_index += 1

        # White category actions
        for category in ["white", "yellow", "blue",
                         "green", "orange", "purple"]:

            action = {"action_type": "need_category", "category": category}
            self.action_to_game[action_index] = action
            action_index += 1

        # Placement actions
        # Placement action for yellow
        for value in range(1, 7):
            for occurrence in [0, 1]:

                action = {
                    "action_type": "enter_yellow",
                    "value": value,
                    "occurrence": occurrence
                }
                self.action_to_game[action_index] = action
                action_index += 1

        # Placemten action for blue
        for value in range(2, 13):

            action = {
                "action_type": "enter_blue",
                "value": value
            }
            self.action_to_game[action_index] = action
            action_index += 1

        # Placement action for green
        action = {"action_type": "enter_green"}
        self.action_to_game[action_index] = action
        action_index += 1

        # Placement action for orange
        action = {"action_type": "enter_orange"}
        self.action_to_game[action_index] = action
        action_index += 1

        # Placement action for purple
        action = {"action_type": "enter_purple"}
        self.action_to_game[action_index] = action
        action_index += 1

        self.action_space_size = action_index

    def reset(self) -> np.array:
        '''
        Reset environment and return to initial observation
        '''
        self.game.reset()
        return self._get_observation()

    def step(self, action_index: int) -> Tuple[np.ndarray, float, bool, Dict]:
        '''
        Execute action and return (observation, reward, done, info)
        '''
        # Convert action index to game action
        game_action = self.action_to_game[action_index]

        # Execute in game
        state, reward, done, info = self.game.step(game_action)

        # Convert state to observation
        observation = self._get_observation()

        return observation, reward, done, info

    def _get_observation(self) -> np.ndarray:
        '''
        Convert game state to numerical observation vector.
        '''
        state = self.game.get_state()
        observation_parts = []

        # Dice values normalised to 0 - 1
        for die_name in ["white", "yellow", "blue",
                         "green", "orange", "purple"]:
            observation_parts.append(state["dice_values"][die_name] / 6.0)

        # Dice states one-hot encoded
        for die_name in ["white", "yellow", "blue",
                         "green", "orange", "purple"]:

            die_state = state["dice_states"][die_name]
            observation_parts.extend([
                1.0 if die_state == "hand" else 0.0,
                1.0 if die_state == "platter" else 0.0,
                1.0 if die_state == "chosen" else 0.0,
            ])

        # Round and Throw info
        observation_parts.append(state["current_round"] / 6.0)
        observation_parts.append(state["current_throw"] / 3.0)

        # Flattening each category's grid
        # Yelllow gird -> 4x4, so 16 cells
        yellow_grid = state["yellow_grid"]
        for row in yellow_grid:
            for cell in row:

                if cell == 'x':
                    observation_parts.append(1.0)
                elif isinstance(cell, int):
                    observation_parts.append(0.0)  # Not crossed yet
                else:
                    observation_parts.append(0.0)

        # Blue grid -> 3x4 with one empty cell, so 11 cells
        blue_grid = state["blue_grid"]
        for row in blue_grid:
            for cell in row:

                if cell == 'x':
                    observation_parts.append(1.0)
                elif cell == '':
                    observation_parts.append(0.0)  # Empty cell
                elif isinstance(cell, int):
                    observation_parts.append(0.0)  # Not crossed yet
                else:
                    observation_parts.append(0.0)

        # Green row -> 11 positions
        green_row = state["green_row"]
        green_index = state["green_index"]
        for i in range(1, 12):

            if green_row[i] == 'x':
                observation_parts.append(1.0)
            else:
                observation_parts.append(0.0)
        # Include normalized current index position
        observation_parts.append(green_index / 11.0)

        # Orange row -> 11 positions
        orange_row = state["orange_row"]
        orange_index = state["orange_index"]
        for i in range(1, 12):
            # Normalize actual values -> 0-6 for die & 0-18 for x3
            observation_parts.append(orange_row[i] / 18.0)
        # Include normalized current index position
        observation_parts.append(orange_index / 11.0)

        # Purple row - 11 positions
        purple_row = state["purple_row"]
        purple_index = state["purple_index"]
        for i in range(1, 12):
            # Normalize actual values -> 0-6
            observation_parts.append(purple_row[i] / 6.0)
        # Include normalized current index position
        observation_parts.append(purple_index / 11.0)

        return np.array(observation_parts, dtype=np.float32)

    def get_valid_actions(self) -> List[int]:
        '''
        Return list of valid action indices for current game state
        '''
        legal_game_actions = self.game.get_legal_actions()
        valid_actions_indices = []

        for game_action in legal_game_actions:

            # Find the corresponding action index
            for action_index, mapped_action in self.action_to_game.items():

                if self._actions_match(game_action, mapped_action):
                    valid_actions_indices.append(action_index)
                    break

        return valid_actions_indices

    def _actions_match(self, action1, action2):
        '''
        Validate if two action dictionaries represent the same action
        '''
        if action1["action_type"] != action2["action_type"]:
            return False

        # Check if all keys match
        if set(action1.keys()) != set(action2.keys()):
            return False

        # Check if all values match
        for key in action1:

            if action1[key] != action2[key]:
                return False

        return True
