
from framework.devices.device import Device
from framework.devices.dolphin.dolphin_pad import DolphinPad


class Dolphin(Device):

    def __init__(self):
        self.pad = DolphinPad()
        super().__init__('dolphin')

    def open(self):
        # Device is already running, nothing to do here
        if self.is_open:
            return

        self.is_open = True

    def close(self):
        if not self.is_open:
            return
