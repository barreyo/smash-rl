
import logging
import time
from typing import List

from transitions import Machine

from framework.agent import Agent
from framework.devices.device import Device
from framework.games.game import Game
from framework.games.ssbm.ssbm_menu_helper import SSBMMenuHelper
from framework.games.ssbm.ssbm_observation import Position, SSBMObservation
from framework.games.ssbm.ssbm_reward import SimpleSSBMReward

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


# TODO: Add all SSBM sub classes, use this as a configuration object for the
#       agent
class SSBMGame(Game):

    STATES = ['not_started', 'start_menu',
              'character_selection', 'character_preselection',
              'stage_selection', 'game_launched', 'game_done']

    STALE_OBSERVATION_TIMEOUT = 5.0

    def __init__(self,
                 device: Device,
                 agents: List[Agent],
                 sampling_window: float,
                 stats_file=None):
        super().__init__(device, agents=agents, stats_file=stats_file)
        self.sampling_window = sampling_window
        self.machine = self._build_state_machine()
        self.menu_helper = SSBMMenuHelper(self.device.pad)
        self.reward_calculator = SimpleSSBMReward()
        self.all_obervations = []
        self.reset_state()

    def _build_state_machine(self):
        machine = Machine(model=self,
                          states=self.STATES,
                          initial='not_started')
        machine.add_transition(trigger='reset_state_machine',
                               source='*',
                               dest=machine.initial)

        # Regular mode
        machine.add_transition(trigger='device_ready',
                               source='not_started',
                               dest='start_menu')
        machine.add_transition(trigger='select_characters',
                               source='start_menu',
                               dest='character_selection')

        # Netplay mode (jumps straight into character selection)
        machine.add_transition(trigger='netplay',
                               source='not_started',
                               dest='character_selection')

        machine.add_transition(trigger='select_stage',
                               source='character_selection',
                               dest='stage_selection')
        machine.add_transition(trigger='launch_game',
                               source='stage_selection',
                               dest='game_launched')
        machine.add_transition(trigger='finish_game',
                               source='game_launched',
                               dest='game_done')
        machine.add_transition(trigger='restart_game',
                               source='game_done',
                               dest='character_preselection')
        machine.add_transition(trigger='preselect_select_stage',
                               source='character_preselection',
                               dest='stage_selection')

        return machine

    def meta_update(self, update_data):

        if not self.prev_meta_updates or \
                self.prev_meta_updates[-1] != update_data:
            self.prev_meta_updates.append(update_data)
        print(self.prev_meta_updates)

        if update_data == 6 and self.state == 'not_started':
            # Enter actual gameplay
            self.netplay()

        if self.prev_meta_updates[-3:] == [13, 11, 12] and \
                self.state == 'game_launched':
            self.stats.append(self.total_game_reward,
                              self.frame_counter)
            log.info(f'GAME STATS: {self.stats.data_store}')
            self.save_agents()
            self.finish_game()

    def game_update(self, observation):
        if self.state != 'game_launched':
            return

        # Wait for stock information
        if observation.player_stocks == 0 and \
                observation.enemy_stocks == 0:
            return

        self.update_agents(observation)

    def hard_reset(self):
        self.reset_state()
        self.reset_state_machine()

    def reset_state(self):
        self.last_update = time.time()
        self.frame_counter = 0
        self.all_obervations = []
        self.total_game_reward = 0
        self.prev_meta_updates = []

        if self.device.pad.is_connected():
            self.device.pad.reset_button_state()

    def restart(self):
        self.reset_state()
        self.restart_game()

    def save_agents(self):
        for agent in self.agents:
            agent.save()

    def update_agents(self, observation: SSBMObservation):
        for agent in self.agents:
            action = agent.act(observation, self.frame_counter)
            # print(f"Should take action: {action}")
            self.device.set_button_state(action.as_slippi_bitmask())

            if self.all_obervations:
                reward = self.reward_calculator.cost(
                    observation, self.all_obervations, self.frame_counter)
                self.total_game_reward += reward
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

    def _is_done(self, observation: SSBMObservation):
        return observation.player_stocks <= 0 or \
            observation.enemy_stocks <= 0

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
        self.restart()
