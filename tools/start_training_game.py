
import pdb
import time

from framework.devices.dolphin.dolphin_pad import DolphinPad
from slippi.event import Buttons

pad = DolphinPad('/Users/kostas/Library/Application Support/Dolphin/Pipes/pipe')

# pad.press_release_button(Buttons.Logical.START)
# time.sleep(2)
# pad.press_release_button(Buttons.Logical.START)
# time.sleep(5)
# pad.press_release_button(Buttons.Logical.A)
# time.sleep(2)
# pad.press_release_button(Buttons.Logical.DPAD_DOWN)
# time.sleep(1)
# pad.press_release_button(Buttons.Logical.DPAD_DOWN)
# time.sleep(1)
# pad.press_release_button(Buttons.Logical.DPAD_DOWN)
# time.sleep(1)
# pad.press_release_button(Buttons.Logical.A)
# pdb.set_trace()


while True:
    pad.press_release_button(Buttons.Logical.DPAD_DOWN)
    # time.sleep(1.0/30.0)
