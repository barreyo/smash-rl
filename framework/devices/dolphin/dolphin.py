
import binascii
import configparser
import errno
import logging
import os
import pkgutil
import shutil
import socket
import subprocess
import time
from pathlib import Path
from typing import Text

from framework.devices.device import Device
from framework.devices.dolphin.dolphin_pad import DolphinPad
from framework.devices.dolphin.exceptions import DolphinNotFoundError

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class Dolphin(Device):

    def __init__(self, executable_path: Path, iso_path: Path, memory_mapping: Path, render: bool = True):
        super().__init__('dolphin')
        self.dolphin_path = self.__get_dolphin_home_path()
        self.fifo_path = self.__create_fifo_pipe('pipe')
        self.memory_mapping_file = memory_mapping
        self.executable_path = executable_path
        self.iso_path = iso_path
        self.render = render
        self.pad = DolphinPad(self.fifo_path)

        # Make sure all config files exist and have correct content
        self.__create_controller_config()
        self.__create_dolphin_config()
        self.__create_memory_watcher()

    def __create_memory_watcher(self):
        # Create config and socket dir
        watcher_dir = self.dolphin_path / 'MemoryWatcher'
        watcher_dir.mkdir(exist_ok=True)
        watcher_path = watcher_dir / 'MemoryWatcher'

        # Create memory locations file
        mem_file = watcher_dir / 'Locations.txt'
        shutil.copy(str(self.memory_mapping_file), str(mem_file))

        # Bind the socket
        try:
            watcher_path.unlink()
        except IOError:
            pass
        self.mem_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.mem_socket.bind(str(watcher_path))
        self.mem_socket.setblocking(False)  # Nonblocking

    def __create_dolphin_config(self):
        dolphin_config_path = self.dolphin_path / 'Config' / 'Dolphin.ini'
        config = configparser.SafeConfigParser()
        config.read(dolphin_config_path)

        # Dolphin config
        # config.set('Core', 'SIDevice', )
        config.set('Core', 'enablecheats', 'True')
        config.set('Input', 'backgroundinput', 'True')
        with open(dolphin_config_path, 'w') as dcp:
            config.write(dcp)

        # TODO: Move this into the game
        # Game specific config
        melee_config_path = self.dolphin_path / "GameSettings" / "GALE01.ini"
        config = configparser.SafeConfigParser(allow_no_value=True)
        config.optionxform = str
        config.read(melee_config_path)
        if not config.has_section("Gecko_Enabled"):
            config.add_section("Gecko_Enabled")
        config.set("Gecko_Enabled", "$Netplay Community Settings")
        with open(melee_config_path, 'w') as dolphinfile:
            config.write(dolphinfile)

    def __create_fifo_pipe(self, fifo_name: Text) -> Text:
        pipes_dir = self.dolphin_path / 'Pipes'
        fifo_path = pipes_dir / fifo_name

        if not pipes_dir.is_dir():
            pipes_dir.mkdir()

        if fifo_path.exists():
            return

        fifo_path = str(fifo_path)
        try:
            os.mkfifo(fifo_path)
        except OSError:
            raise

        return fifo_path

    def __create_controller_config(
            self, pad_name='GCPad', config_file_name='pipe.ini') -> None:
        # Load the pre-defined controller config that our code expects
        default_config = pkgutil.get_data(__package__, 'config/pipe.ini')
        if default_config is None:
            raise IOError('Default config file missing in project')
        config_text = default_config.decode()

        pad_dir = self.dolphin_path / 'Config' / 'Profiles' / pad_name
        if not pad_dir.is_dir():
            pad_dir.mkdir(parents=True)

        output_dir = pad_dir / config_file_name
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

    def launch(self):
        # Device is already running, nothing to do here
        if self.is_open:
            return

        command = [str(self.executable_path)]
        if not self.render:
            command.append("-v")
            command.append("Null")  # Use the "Null" renderer

        command.append("-u")
        command.append(str(self.dolphin_path))

        command.append("-e")
        command.append(str(self.iso_path))
        log.info(f"Starting dolphin with: {' '.join(command)}")

        self.process = subprocess.Popen(command)
        time.sleep(10)
        log.info("Dolphin launched")

        # Set up controller
        self.pad.connect()
        self.is_open = True

    def read_state(self):
        data = None
        try:
            data = self.mem_socket.recvfrom(
                9096)[0].decode('utf-8').splitlines()
        except socket.timeout:  # Won't happen with nonblocking
            return None, None
        except socket.error as e:
            if e.errno != errno.EAGAIN:
                raise e

        # Strip the null terminator, pad with zeros, then convert to bytes
        if data is not None:
            return data[0], binascii.unhexlify(data[1].strip('\x00').zfill(8))
        else:
            return None, None

    def set_button_state(self, state):
        self.pad.set_button_state(state)

    def terminate(self):
        if not self.is_open:
            return

        if self.process != None:
            self.process.terminate()

        self.is_open = False

    def __del__(self):
        try:
            if self.mem_socket is not None:
                self.mem_socket.close()
        except AttributeError:
            pass

        try:
            self.terminate()
        except:
            pass

        self.process = None
        self.mem_socket = None
