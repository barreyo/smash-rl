
import time
from struct import pack, unpack
from typing import List

from framework.agent import Agent
from framework.devices.device import Device
from framework.games.game import Game
from framework.games.ssbm.ssbm_observation import SSBMObservation


def int_to_float(i):
    return unpack('<f', pack('<I', i))[0]


ADDRESS_TO_PROPERTY = {
    '8045310E': ('>I', 24, None, 'player_stocks'),
    '80453F9E': ('>I', 24, None, 'enemy_stocks'),
    '804530E0': ('>I', 16, None, 'player_percent'),
    '80453F70': ('>I', 16, None, 'enemy_percent'),
    '80453090': ('>f', 0, None, 'player_x'),
    '80453094': ('>f', 0, None, 'player_y'),
    '80453F20': ('>f', 0, None, 'enemy_x'),
    '80453F24': ('>f', 0, None, 'enemy_y'),
    # '8046B6CC': ('<I', 0, 'frame')
}


# TODO: Add all SSBM sub classes, use this as a configuration object for the
#       agent
class SSBMGame(Game):

    def __init__(self, device: Device, agents: List[Agent] = []):
        super().__init__(device, agents=agents)
        self.current_observation = SSBMObservation()
        self.timestamp = 0
        self.frame_counter = 0

    def run(self):
        while True:
            address, value = self.device.read_state()
            self.update_observation(address, value)

    def update_agents(self, observation, frame):
        new_time = time.time()
        if new_time - self.timestamp > 0.05:  # 50ms
            self.timestamp = new_time
            for agent in self.agents:
                action = agent.act(observation, self.frame_counter)
                print(f"Should take action: {action}")
                self.device.set_button_state(action.as_slippi_bitmask())

            self.frame_counter += 1

            # TODO: Send action back

    def update_observation(self, address, buffer):
        operator, bit_shift, transform_fn, property_name = \
            ADDRESS_TO_PROPERTY[address]
        value = unpack(operator, buffer)[0]
        if bit_shift > 0:
            value = value >> bit_shift

        setattr(self.current_observation, property_name, value)
        self.update_agents(self.current_observation, value)
