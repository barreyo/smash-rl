
import argparse
from pathlib import Path

from framework.devices.dolphin.dolphin import Dolphin
from framework.games.ssbm.ssbm import SSBMGame
from smashrl.ssbm_agent import SSBMAgent


class Session():

    SAMPLING_WINDOW = 1.0/15.0

    def __init__(self, args):
        self.agent = SSBMAgent(inference_only=True)
        self.agent.load()
        self.device = Dolphin(
            executable_path=Path(args.dolphin_bin),
            iso_path=Path(args.game_iso),
            memory_mapping=Path(
                "./framework/devices/dolphin/config/Locations.txt"),
            render=True
        )
        self.game = SSBMGame(self.device, [self.agent], self.SAMPLING_WINDOW)

    def start_session(self):
        self.device.launch()
        self.game.netplay()

        while True:
            self.game.run()
            self.game.reset()
        # self.device.close()
        # return self.game.result


def __main():
    parser = argparse.ArgumentParser(
        description='Launch Dolphin and setup AI agent.'
    )
    parser.add_argument('--dolphin-bin', dest='dolphin_bin',
                        help='Path to Dolphin binary')
    parser.add_argument('--game-iso', dest='game_iso',
                        help='Path to game ISO file')

    args = parser.parse_args()
    session = Session(args)
    session.start_session()


if __name__ == "__main__":
    __main()
