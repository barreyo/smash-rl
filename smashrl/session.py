
from pathlib import Path

from framework.devices.dolphin.dolphin import Dolphin
from framework.games.ssbm.ssbm import SSBMGame
from smashrl.ssbm_agent import SSBMAgent


class Session():

    def __init__(self):
        self.agent = SSBMAgent(inference_only=True)
        self.agent.load()
        self.device = Dolphin(Path("/Users/kostas/Projects/smash-rl/framework/devices/dolphin/config/Locations.txt"))
        self.game = SSBMGame(self.device, [self.agent])

    def start_game(self):
        # self.device.open()
        self.game.run()
        # self.device.close()
        # return self.game.result


def __main():
    session = Session()
    session.start_game()


if __name__ == "__main__":
    __main()
