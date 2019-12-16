
import argparse
import logging
from pathlib import Path

from framework.devices.dolphin.dolphin import Dolphin
from framework.games.exceptions import StaleDeviceError
from framework.games.ssbm.ssbm import SSBMGame
from smashrl.ssbm_agent import SSBMAgent
from framework.game_session import GameSession
from framework.state_builders import SSBMDolphinBuilder

log = logging.getLogger(__name__)


class Session():

    SAMPLING_WINDOW = 1.0/15.0

    def __init__(self, args):
        self.agent = SSBMAgent(inference_only=False)
        self.agent.load()
        self.device = Dolphin(
            executable_path=Path(args.dolphin_bin),
            iso_path=Path(args.game_iso),
            memory_mapping=Path(
                "./framework/devices/dolphin/config/Locations.txt"),
            render=True
        )
        self.game = SSBMGame(
            self.device, [self.agent], self.SAMPLING_WINDOW,
            stats_file='stats.json')
        self.game_session = GameSession(
            self.agent, self.device, self.game, SSBMDolphinBuilder())

        self.game_session.start()

#    def start_session(self):
        # self.game.netplay()

        # while True:
        #    try:
        #        self.game.run()
        #        self.game.restart()
        #    except StaleDeviceError:
        #        log.info("Device is stale, restarting...")
        #        self.device.restart()
        #        self.game.hard_reset()
        #        self.game.netplay()

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
    Session(args)


if __name__ == "__main__":
    __main()
