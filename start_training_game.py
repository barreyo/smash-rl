import logging
from smashrl.game_controller import Pad
from slippi.event import Buttons
import time


with Pad('/Users/kostas/Library/Application Support/Dolphin/Pipes/pipe') as pad:
  pad.press_release_button(Buttons.Logical.START)
  time.sleep(5)
  pad.press_release_button(Buttons.Logical.START)
  time.sleep(5)
  pad.press_release_button(Buttons.Logical.A)
  time.sleep(2)
  pad.press_release_button(Buttons.Logical.DPAD_DOWN)
  time.sleep(1)
  pad.press_release_button(Buttons.Logical.DPAD_DOWN)
  time.sleep(1)
  pad.press_release_button(Buttons.Logical.DPAD_DOWN)
  time.sleep(1)
  pad.press_release_button(Buttons.Logical.A)
  import pdb; pdb.set_trace()
