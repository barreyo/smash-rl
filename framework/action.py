
class Action():

    def as_array(self):
        raise NotImplementedError("Implement as_array for your action")


class DiscreteAction(Action):
    pass


class ContinuousAction(Action):
    pass
