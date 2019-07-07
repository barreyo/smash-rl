
import copy
import logging
import time
from struct import pack, unpack
from typing import List

from transitions import Machine

from framework.agent import Agent
from framework.devices.device import Device
from framework.games.exceptions import StaleDeviceError
from framework.games.game import Game
from framework.games.ssbm.ssbm_menu_helper import SSBMMenuHelper
from framework.games.ssbm.ssbm_observation import Position, SSBMObservation
from framework.games.ssbm.ssbm_reward import SimpleSSBMReward

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def int_to_float(i):
    return unpack('<f', pack('<I', i))[0]


ADDRESS_TO_PROPERTY = {
    '8045310E': ('>I', 24, 'player_stocks'),
    '80453F9E': ('>I', 24, 'enemy_stocks'),
    '804530E0': ('>I', 16, 'player_percent'),
    '80453F70': ('>I', 16, 'enemy_percent'),
    '80453090': ('>f', 0, 'player_x'),
    '80453094': ('>f', 0, 'player_y'),
    '80453F20': ('>f', 0, 'enemy_x'),
    '80453F24': ('>f', 0, 'enemy_y'),
}


# TODO: Add all SSBM sub classes, use this as a configuration object for the
#       agent
class SSBMGame(Game):

    STATES = ['not_started', 'start_menu',
              'character_selection', 'character_preselection', 'stage_selection', 'game_launched', 'game_done']

    STALE_OBSERVATION_TIMEOUT = 5.0

    def __init__(self, device: Device, agents: List[Agent], sampling_window: float):
        super().__init__(device, agents=agents)
        self.sampling_window = sampling_window
        self.machine = self._build_state_machine()
        self.menu_helper = SSBMMenuHelper(self.device.pad)
        self.reward_calculator = SimpleSSBMReward()
        self.all_obervations = []
        self.reset_state()

    def _build_state_machine(self):
        machine = Machine(model=self, states=self.STATES,
                          initial='not_started')
        machine.add_transition(trigger='reset_state_machine', source='*', dest=machine.initial)

        # Regular mode
        machine.add_transition(trigger='device_ready',
                               source='not_started', dest='start_menu')
        machine.add_transition(trigger='select_characters',
                               source='start_menu', dest='character_selection')

        # Netplay mode (jumps straight into character selection)
        machine.add_transition(trigger='netplay',
                               source='not_started', dest='character_selection')

        machine.add_transition(
            trigger='select_stage', source='character_selection', dest='stage_selection')
        machine.add_transition(trigger='launch_game',
                               source='stage_selection', dest='game_launched')
        machine.add_transition(trigger='finish_game',
                               source='game_launched', dest='game_done')
        machine.add_transition(trigger='restart_game',
                               source='game_done', dest='character_preselection')
        machine.add_transition(trigger='preselect_select_stage',
                               source='character_preselection', dest='stage_selection')

        return machine

    def run(self):
        assert self.state == 'game_launched'

        run_time = time.time()

        while True:
            address, value = self.device.read_state()
            if address is not None:  # None if socket times out first
                self.update_observation(address, value)

            # Wait for stock information
            if self.current_observation.player_stocks > 0 and \
               self.current_observation.enemy_stocks > 0:
                break

            # If we have not received an observation before the stale timeout, signal to restart
            # We are in an invalid state
            if time.time() > (run_time + self.STALE_OBSERVATION_TIMEOUT):
                self.save_agents()
                raise StaleDeviceError(f'Did not receive updates within {self.STALE_OBSERVATION_TIMEOUT} seconds')

        while True:
            new_time = time.time()
            address, value = self.device.read_state()

            if address is not None:  # None if socket times out first
                self.update_observation(address, value)
                if self._is_done():
                    self.save_agents()
                    self.finish_game()
                    break

            if new_time >= (self.last_update + self.sampling_window):
                self.update_agents(self.current_observation)
                self.last_update = time.time()

    def hard_reset(self):
        self.reset_state()
        self.reset_state_machine()

    def reset_state(self):
        self.current_observation = SSBMObservation()
        self.last_update = time.time()
        self.frame_counter = 0
        self.all_obervations = []

        if self.device.pad.is_connected():
            self.device.pad.reset_button_state()

    def restart(self):
        self.reset_state()
        self.restart_game()

    def save_agents(self):
        for agent in self.agents:
            agent.save()

    def update_agents(self, observation):
        for agent in self.agents:
            action = agent.act(observation, self.frame_counter)
            # print(f"Should take action: {action}")
            self.device.set_button_state(action.as_slippi_bitmask())

            if self.all_obervations:
                reward = self.reward_calculator.cost(
                    observation, self.all_obervations, self.frame_counter)
                agent.learn(self.all_obervations[-1],
                            observation, action, reward, 0.0)
                print(f'Reward: {reward}')

        previous_observation = SSBMObservation(
            Position(observation.player_x, observation.player_y),
            Position(observation.enemy_x, observation.enemy_y),
            observation.player_stocks, observation.enemy_stocks,
            observation.player_percent, observation.enemy_percent)
        self.all_obervations.append(previous_observation)
        self.frame_counter += 1

    def update_observation(self, address, buffer):
        operator, bit_shift, property_name = \
            ADDRESS_TO_PROPERTY[address]
        value = unpack(operator, buffer)[0]
        if bit_shift > 0:
            value = value >> bit_shift

        setattr(self.current_observation, property_name, value)

    def _is_done(self):
        return self.current_observation.player_stocks <= 0 or \
            self.current_observation.enemy_stocks <= 0

    def on_enter_start_menu(self):
        self.menu_helper.go_to_character_select()
        time.sleep(2)
        self.select_characters()

    def on_enter_character_selection(self):
        self.menu_helper.select_characters()
        self.select_stage()

    def on_enter_stage_selection(self):
        self.menu_helper.select_stage()
        self.launch_game()

    def on_enter_game_launched(self):
        self.menu_helper.start_game()

    def on_enter_character_preselection(self):
        self.menu_helper.exit_stats_screen()
        self.preselect_select_stage()

    def on_exit_character_preselection(self):
        time.sleep(3)
        self.menu_helper.preselect_characters()
        time.sleep(2)

    def on_enter_game_done(self):
        time.sleep(5)  # Wait for stats screen to appear
