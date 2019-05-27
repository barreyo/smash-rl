
import os
import pkgutil
from pathlib import Path
from typing import Text

from framework.devices.device import Device
from framework.devices.dolphin.dolphin_pad import DolphinPad
from framework.devices.dolphin.exceptions import DolphinNotFoundError


class Dolphin(Device):

    def __init__(self):
        super().__init__('dolphin')
        self.dolphin_path = self.__get_dolphin_home_path()
        self.fifo_path = self.__create_fifo_pipe('pipe')
        self.pad = DolphinPad(self.fifo_path)

        self.__create_controller_config()

    def __create_dolphin_config(self):
        pass

    def __create_fifo_pipe(self, fifo_name: Text) -> Text:
        pipes_dir = self.dolphin_path / 'Pipes'
        fifo_path = str(pipes_dir / fifo_name)

        if not pipes_dir.is_dir():
            pipes_dir.mkdir()

        try:
            os.mkfifo(fifo_path)
        except OSError:
            # Try deleting the socket file and recreate it on error
            Path(fifo_path).unlink()
            os.mkfifo(fifo_path)

        # Try opening the pipe to make sure everything is nice and dandy
        self.fifo_pipe = open(fifo_path)
        return fifo_path

    def __create_controller_config(
            self, pad_name='GCPad', config_file_name='pipe.ini') -> None:
        # Load the pre-defined controller config that our code expects
        default_config = pkgutil.get_data(__package__, 'config/pipe.ini')
        if default_config is None:
            raise IOError('Default config file missing in project')
        config_text = default_config.decode()
        output_dir = (self.dolphin_path / 'Config' / 'Profiles' /
                      pad_name / config_file_name)
        output_dir.write_text(config_text)

    def __get_dolphin_home_path(self) -> Path:
        home_dir = Path.home()

        # Linux legacy
        linux_legacy_path = home_dir / '.dolphin-emu'
        if linux_legacy_path.is_dir():
            return linux_legacy_path

        # OS X
        osx_path = home_dir / 'Library' / 'Application Support' / 'Dolphin'
        if osx_path.is_dir():
            return osx_path

        # Linux
        linux_path = home_dir / '.local' / 'share' / 'dolphin-emu'
        if linux_path.is_dir():
            return linux_path

        # Windows
        raise DolphinNotFoundError(
            "Dolphin emulator could not be found on the system. "
            "Please install Dolphin and try again.")

    def open(self):
        # Device is already running, nothing to do here
        if self.is_open:
            return

        self.is_open = True

    def close(self):
        if not self.is_open:
            return

        self.is_open = False
