
import time
import logging

from framework.agent import Agent
from framework.devices.device import Device
from framework.games.game import Game
from framework.state_builders import StateBuilder

log = logging.getLogger(__name__)


class GameSession():

    SAMPLING_WINDOW = 1.0/15.0  # Seconds
    STALE_OBSERVATION_TIMEOUT = 20  # Seconds

    def __init__(self, agent: Agent, device: Device, game: Game,
                 builder: StateBuilder):
        self.agent = agent
        self.device = device
        self.game = game
        self.device_update_builder = builder
        self.last_update = time.time()

    def start(self):
        self.device.launch()
        last_meta_update = time.time()

        while True:
            new_time = time.time()
            vals = self.device.read_state()
            meta_update, game_update = self.device_update_builder.transform(
                vals)

            # If we have not received an observation before the stale timeout,
            # signal to restart
            # We are in an invalid state
            if new_time > (last_meta_update +
                           self.STALE_OBSERVATION_TIMEOUT):
                log.warning('Stale device detected. Restarting device...')
                self.device.restart()
                self.game.hard_reset()
                last_meta_update = time.time()
                continue

            if meta_update is not None:
                self.game.meta_update(meta_update)
                last_meta_update = time.time()

            if new_time >= (self.last_update + self.SAMPLING_WINDOW):

                if game_update is not None:
                    self.game.game_update(game_update)

                self.last_update = time.time()
