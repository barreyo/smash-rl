

class Device():

    def __init__(self, device_name):
        self.device_name = device_name
        self.is_open = False

    def open(self):
        raise NotImplementedError("Implement open() function")

    def close(self):
        raise NotImplementedError("Implement close() function")

    def read_state(self):
        raise NotImplementedError("Implement read_state() function")
