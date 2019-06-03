import time

from slippi.event import Buttons


class SSBMMenuHelper:

    def __init__(self, pad):
        self.pad = pad

    def go_to_character_select(self):
        self.pad.press_release_button(Buttons.Logical.START)
        time.sleep(2)
        self.pad.press_release_button(Buttons.Logical.START)
        time.sleep(4)
        self.pad.press_release_button(Buttons.Logical.DPAD_DOWN)
        time.sleep(2)
        self.pad.press_release_button(Buttons.Logical.A)
        time.sleep(1)
        self.pad.press_release_button(Buttons.Logical.A)
        time.sleep(1)

    def select_characters(self):
        # Select Fox
        self.pad.press_release_button(Buttons.Logical.JOYSTICK_UP, 0.22)
        self.pad.press_release_button(Buttons.Logical.JOYSTICK_RIGHT, 0.05)
        self.pad.press_release_button(Buttons.Logical.A, 0.1)

        # Select p2 as CPU
        self.pad.press_release_button(Buttons.Logical.JOYSTICK_RIGHT, 0.05)
        self.pad.press_release_button(Buttons.Logical.JOYSTICK_DOWN, 0.09)
        self.pad.press_release_button(Buttons.Logical.A)

    def select_stage(self):
        pass

    def start_game(self):
        pass
