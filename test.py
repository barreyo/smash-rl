import logging
from smashrl.game_controller import Pad
from slippi.event import Buttons
import time

pad = Pad('/Users/kostas/Library/Application Support/Dolphin/Pipes/pipe')
pad.logger.setLevel(logging.DEBUG)
# p.set_button_state(Buttons.Logical.JOYSTICK_LEFT)
# p.set_button_state(Buttons.Logical.JOYSTICK_UP)
pad.reset_button_state()
# p.set_button_state(Buttons.Logical.A)
pad.set_button_state(Buttons.Logical.B)
time.sleep(1)
pad.set_button_state(Buttons.Logical.NONE)