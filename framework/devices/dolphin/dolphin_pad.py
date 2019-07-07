
import functools
import logging
import time

from slippi.event import Buttons  # TODO: Move in to "dolphin"?

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


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
            Buttons.Logical.CSTICK_DOWN: [0.5, 0],
            Buttons.Logical.CSTICK_LEFT: [0, 0.5],
            Buttons.Logical.CSTICK_RIGHT: [1, 0.5],
            Buttons.Logical.CSTICK_UP: [0.5, 1],
        },
        'MAIN': {
            Buttons.Logical.JOYSTICK_DOWN: [0.5, 0],
            Buttons.Logical.JOYSTICK_LEFT: [0, 0.5],
            Buttons.Logical.JOYSTICK_RIGHT: [1, 0.5],
            Buttons.Logical.JOYSTICK_UP: [0.5, 1],
        }
    }
    ALL_CONTINUOUS_BUTTONS = functools.reduce(
        lambda x, y: x + list(y.keys()), list(CONTINUOUS_BUTTONS.values()), [])

    MIN_COOLDOWN = 1.0/30.0

    def __init__(self, path):
        log.info("Attaching Pad to Dolphin")
        self.path = path
        self.prev = Buttons.Logical.NONE
        self.last_command_time = time.time()
        self.pipe = None

    def __del__(self, *args):
        """Closes the fifo."""
        try:
            self.pipe.close()
        except:
            pass

    def connect(self):
        self.pipe = open(self.path, 'w', buffering=1)

    def is_connected(self):
        return self.pipe is not None

    def _send_to_pipe(self, msg):
        # log.info(msg)
        current_time = time.time()
        sleep_time = self.last_command_time + self.MIN_COOLDOWN - current_time
        if sleep_time > 0:
            time.sleep(sleep_time)
        self.last_command_time = time.time()
        self.pipe.write('{}\n'.format(msg))

    def _get_button_name(self, button):
        if button in self.BUTTONS_TO_CONTROLLER:
            return self.BUTTONS_TO_CONTROLLER[button]
        return button.name

    def set_button_state(self, button_state: Buttons.Logical):
        diff = self.prev ^ button_state  # prev XOR new
        press = diff & button_state  # Send press for: diff AND new
        release = diff & self.prev  # Send release for: diff AND pref
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

    def press_release_button(self, button, min_timeout=0):
        """Press and release a button. This is only for testing, don't use."""
        assert button in Buttons.Logical
        self.press_button(button)
        if min_timeout > 0:
            time.sleep(min_timeout)
        self.release_button(button)

    def press_button(self, button):
        """Press a button."""
        assert button in Buttons.Logical

        # Button pressed is a continuous button, but we will just
        # set the max value
        if button in self.ALL_CONTINUOUS_BUTTONS:
            if button in self.CONTINUOUS_BUTTONS['C'].keys():
                self._send_to_pipe('SET {} {:.2f} {:.2f}'.format(
                    'C', *self.CONTINUOUS_BUTTONS['C'][button]))
            elif button in self.CONTINUOUS_BUTTONS['MAIN'].keys():
                self._send_to_pipe('SET {} {:.2f} {:.2f}'.format(
                    'MAIN', *self.CONTINUOUS_BUTTONS['MAIN'][button]))
            else:
                raise Exception('Unidentified button sent')
        else:
            self._send_to_pipe('PRESS {}'.format(
                self._get_button_name(button)))

    def release_button(self, button):
        """Release a button."""
        assert button in Buttons.Logical
        if button in self.CONTINUOUS_BUTTONS['C'].keys():
            self._send_to_pipe('SET C 0.5 0.5')
        elif button in self.CONTINUOUS_BUTTONS['MAIN'].keys():
            self._send_to_pipe('SET MAIN 0.5 0.5')
        else:
            self._send_to_pipe('RELEASE {}'.format(
                self._get_button_name(button)))
