
from pathlib import Path

from framework.devices.dolphin.dolphin import Dolphin
from framework.games.ssbm.ssbm import SSBMGame
from smashrl.ssbm_agent import SSBMAgent


class Session():

    SAMPLING_WINDOW = 1.0/15.0

    def __init__(self):
        self.agent = SSBMAgent(inference_only=True)
        self.agent.load()
        self.device = Dolphin(
            executable_path=Path("/Users/kostas/Projects/dolphin/build//Binaries/Dolphin.app/Contents/MacOS/Dolphin"),
            iso_path=Path("/Users/kostas/Downloads/isos/SSBM.iso"),
            memory_mapping=Path("/Users/kostas/Projects/smash-rl/framework/devices/dolphin/config/Locations.txt"),
            render=True
        )
        self.game = SSBMGame(self.device, [self.agent], self.SAMPLING_WINDOW)

    def start_game(self):
        self.device.launch()
        self.game.device_ready()
        self.game.run()
        # self.device.close()
        # return self.game.result


def __main():
    session = Session()
    session.start_game()


if __name__ == "__main__":
    __main()
