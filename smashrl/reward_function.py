"""Cost/reward function implementations."""


class RewardState():

    def get_cost(self):
        raise NotImplementedError()

    def reset(self):
        raise NotImplementedError()


class SimpleSSMMRewardState(RewardState):

    LIFE_LOSS_COST = -1.0
    LIFE_INFLICT_COST = 1.0
    STOCK_LOSS_COST = -100.0
    STOCK_INFLICT_COST = 100.0
    TIMESTEP_COST = -0.05

    def __init__(self, starting_stock: int):
        self.starting_stock = starting_stock
        self.prev_player_life = 0
        self.prev_enemy_life = 0
        self.prev_player_stock = self.starting_stock
        self.prev_enemy_stock = self.starting_stock

    def get_cost(self, player_life: float, player_stock: int,
                 enemy_life: float, enemy_stock: int, timestep: int) -> float:
        cost = timestep * self.TIMESTEP_COST

        if (self.prev_player_stock - player_stock) > 0:
            cost += (self.prev_player_stock - player_stock) * \
                self.STOCK_LOSS_COST
        else:
            cost += (self.prev_player_life - player_life) * self.LIFE_LOSS_COST

        if (self.prev_enemy_stock - enemy_stock) > 0:
            cost += (self.prev_enemy_stock - enemy_stock) * \
                self.STOCK_INFLICT_COST
        else:
            cost += (self.prev_enemy_life - enemy_life) * \
                self.LIFE_INFLICT_COST

        self.prev_player_life = player_life
        self.prev_player_stock = player_stock
        self.prev_enemy_life = enemy_life
        self.prev_enemy_stock = enemy_stock

        return cost

    def reset(self):
        self.prev_player_life = 0
        self.prev_enemy_life = 0
        self.prev_player_stock = self.starting_stock
        self.prev_enemy_stock = self.starting_stock
