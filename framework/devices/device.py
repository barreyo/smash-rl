

class Device():

    def __init__(self, device_name):
        self.device_name = device_name
        self.is_open = False

    def launch(self):
        raise NotImplementedError("Implement launch() function")

    def terminate(self):
        raise NotImplementedError("Implement terminate() function")

    def read_state(self):
        raise NotImplementedError("Implement read_state() function")
