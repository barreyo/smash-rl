"""Observation of a single frame."""

from collections import namedtuple

import numpy as np

from framework.observation import Observation

Position = namedtuple('Position', ['x', 'y'])


class SSBMObservation(Observation):
    """Class denoting the state of a frame."""

    def __init__(self, player_pos: Position, enemy_pos: Position,
                 player_stocks: int, enemy_stocks: int, player_percent: float,
                 enemy_percent: float):
        """
        State of a single frame(timestep).

        Arguments:
        player_pos -- Tuple(float, float) with the player position
        enemy_pos -- Tuple(float, float) with enemy position
        player_stocks -- Integer denoting the number of stocks left for the
            player
        enemy_stocks -- Integer denoting the number of stocks left for the
            enemy
        player_percent -- The players' life as percentage
        enemy_percent -- Float denoting enemy's life as percentage

        """
        assert player_stocks >= 0 and enemy_stocks >= 0, \
            "Stocks cannot be negative"
        assert player_percent >= 0.0 and enemy_percent >= 0.0, \
            "Player health percentage has to be a positive value"

        self.player_position = player_pos
        self.enemy_position = enemy_pos
        self.player_stocks = player_stocks
        self.enemy_stocks = enemy_stocks
        self.player_percent = player_percent
        self.enemy_percent = enemy_percent

    def as_array(self) -> np.array:
        """
        Return observation as flattened numpy array.

        Format:
        [px, py, ex, ey, p_stock, e_stock, p_percent, e_percent], where

          'p' denotes player
          'e' denotes enemy
        """
        return np.array([self.player_position.x, self.player_position.y,
                         self.enemy_position.x, self.enemy_position.y,
                         float(self.player_stocks), float(self.enemy_stocks),
                         self.player_percent, self.enemy_percent])

    def __str__(self):  # noqa
        return f'Observation(player_state=({self.player_position}, ' \
               f'{self.player_stocks}, {self.player_percent}), ' \
               f'enemy_state=({self.enemy_position}, {self.enemy_stocks}, ' \
               f'{self.enemy_percent}))'
