import enum
import os
import posix
import subprocess
import logging
import functools
import time

from slippi.event import Buttons # TODO: Move in to "dolphin"?


def bits(n):
    while n:
        b = n & (~n+1)
        yield b
        n ^= b

class DolphinPad:
    """
    Control dolphin emulator through pipes.
    """

    BUTTONS_TO_CONTROLLER = {
        Buttons.Logical.DPAD_DOWN: 'D_DOWN',
        Buttons.Logical.DPAD_UP: 'D_UP',
        Buttons.Logical.DPAD_LEFT: 'D_LEFT',
        Buttons.Logical.DPAD_RIGHT: 'D_RIGHT'
    }

    CONTINUOUS_BUTTONS = {
        'C': {
            Buttons.Logical.CSTICK_DOWN: [0, -1],
            Buttons.Logical.CSTICK_LEFT: [-1, 0],
            Buttons.Logical.CSTICK_RIGHT: [1, 0],
            Buttons.Logical.CSTICK_UP: [0, 1],
        },
        'MAIN': {
            Buttons.Logical.JOYSTICK_DOWN: [0, -1],
            Buttons.Logical.JOYSTICK_LEFT: [-1, 0],
            Buttons.Logical.JOYSTICK_RIGHT: [1, 0],
            Buttons.Logical.JOYSTICK_UP: [0, 1],
        }
    }
    ALL_CONTINUOUS_BUTTONS = functools.reduce(lambda x,y: x + list(y.keys()), list(CONTINUOUS_BUTTONS.values()), [])

    def __init__(self, path):
        self.path = path
        self.logger = logging.getLogger(self.__class__.__name__)
        self.prev = Buttons.Logical.NONE

    def __enter__(self):
        """Opens the fifo. Blocks until the other side is listening."""
        self.pipe = open(self.path, 'w', buffering=1)
        return self

    def __exit__(self, *args):
        """Closes the fifo."""
        if self.pipe:
            self.pipe.close()

    def _send_to_pipe(self, msg):
        self.logger.info(msg)
        print(msg)
        self.pipe.write('{}\n'.format(msg))

    def _get_button_name(self, button):
        if button in self.BUTTONS_TO_CONTROLLER:
            return self.BUTTONS_TO_CONTROLLER[button]
        return button.name

    def set_button_state(self, button_state):
        diff = self.prev ^ button_state # prev XOR new
        press = diff & button_state # Send press for: diff AND new
        release = diff & self.prev # Send release for: diff AND pref
        # keep = self.prev & button_state # Keep pressing: prev AND new
        self.prev = press

        # Release old buttons
        for i in bits(release):
            self.release_button(Buttons.Logical(i))

        # Press new buttons
        for i in bits(press):
            self.press_button(Buttons.Logical(i))

        return press, release

    def reset_button_state(self):
        for button in Buttons.Logical:
            self.release_button(button)

    def press_release_button(self, button):
        """Press and release a button. This is only for testing, don't use"""
        assert button in Buttons.Logical
        self.press_button(button)
        time.sleep(0.1)
        self.release_button(button)

    def press_button(self, button):
        """Press a button."""
        assert button in Buttons.Logical

        # Button pressed is a continuous button, but we will just set the max value
        if button in self.ALL_CONTINUOUS_BUTTONS:
            if button in self.CONTINUOUS_BUTTONS['C'].keys():
                self._send_to_pipe('SET {} {:.2f} {:.2f}'.format('C', *self.CONTINUOUS_BUTTONS['C'][button]))
            elif button in self.CONTINUOUS_BUTTONS['MAIN'].keys():
                self._send_to_pipe('SET {} {:.2f} {:.2f}'.format('MAIN', *self.CONTINUOUS_BUTTONS['MAIN'][button]))
            else:
                raise Exception('Unidentified button sent')
        else:
            self._send_to_pipe('PRESS {}'.format(self._get_button_name(button)))

    def release_button(self, button):
        """Release a button."""
        assert button in Buttons.Logical
        if button in self.ALL_CONTINUOUS_BUTTONS:
            pass # TODO: Fix
        else:
            self._send_to_pipe('RELEASE {}'.format(self._get_button_name(button)))