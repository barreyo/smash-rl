
from framework.devices.dolphin.dolphin import Dolphin
from framework.games.ssbm.ssbm import SSBMGame
from smashrl.ssbm_agent import SSBMAgent


class Session():

    def __init__(self):
        self.agent = SSBMAgent()
        self.device = Dolphin()
        self.game = SSBMGame(self.device, [self.agent])

    def start_game(self):
        self.device.open()
        self.game.enter_game_loop()
        self.device.close()
        return self.game.result


def __main():
    session = Session()
    session.start_game()


if __name__ == "__main__":
    __main()
