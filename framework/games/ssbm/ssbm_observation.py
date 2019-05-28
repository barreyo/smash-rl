"""Observation of a single frame."""

import numpy as np

from framework.observation import Observation


class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"(x={self.x}, y={self.y})"


class SSBMObservation(Observation):
    """Class denoting the state of a frame."""

    @staticmethod
    def size():
        return len(SSBMObservation().as_array())

    def __init__(self,
                 player_pos: Position = Position(x=0, y=0),
                 enemy_pos: Position = Position(x=0, y=0),
                 player_stocks: int = 0,
                 enemy_stocks: int = 0,
                 player_percent: float = 0.0,
                 enemy_percent: float = 0.0):
        """
        State of a single frame(timestep).

        Arguments:
        player_pos -- Tuple(float, float) with the player position
        enemy_pos -- Tuple(float, float) with enemy position
        player_stocks -- Integer denoting the number of stocks left for the
            player
        enemy_stocks -- Integer denoting the number of stocks left for the
            enemy
        player_percent -- The players' knockout percentage (0->inf)
        enemy_percent -- Float denoting enemy's knockout  percentage (0->inf)

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

    @property
    def player_x(self):
        return self.player_position.x

    @player_x.setter
    def player_x(self, val):
        self.player_position.x = val

    @property
    def player_y(self):
        return self.player_position.y

    @player_y.setter
    def player_y(self, val):
        self.player_position.y = val

    @property
    def enemy_x(self):
        return self.enemy_position.x

    @enemy_x.setter
    def enemy_x(self, val):
        self.enemy_position.x = val

    @property
    def enemy_y(self):
        return self.enemy_position.y

    @enemy_y.setter
    def enemy_y(self, val):
        self.enemy_position.y = val

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
