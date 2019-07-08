
from struct import unpack
from framework.games.ssbm.ssbm_observation import SSBMObservation


class StateBuilder():

    def transform(self, generic_data):
        raise NotImplementedError()


class SSBMDolphinBuilder(StateBuilder):

    ADDRESS_TO_PROPERTY = {
        '8045310E': ('>I', 24, 'player_stocks'),
        '80453F9E': ('>I', 24, 'enemy_stocks'),
        '804530E0': ('>I', 16, 'player_percent'),
        '80453F70': ('>I', 16, 'enemy_percent'),
        '80453090': ('>f', 0, 'player_x'),
        '80453094': ('>f', 0, 'player_y'),
        '80453F20': ('>f', 0, 'enemy_x'),
        '80453F24': ('>f', 0, 'enemy_y'),
        '8065CC14': ('>I', 20, 'menu_state'),
    }

    def __init__(self):
        self.observation = SSBMObservation()

    def transform(self, dolphin_data):
        address, buffer = dolphin_data
        meta_update = None

        if address is None:
            return meta_update, self.observation

        operator, bit_shift, property_name = \
            self.ADDRESS_TO_PROPERTY[address]
        value = unpack(operator, buffer)[0]
        if bit_shift > 0:
            value = value >> bit_shift

        setattr(self.observation, property_name, value)

        if address == '8065CC14':
            value = value & 0x0F
            meta_update = value

        return meta_update, self.observation
