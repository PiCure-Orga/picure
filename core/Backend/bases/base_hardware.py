import gpiozero


class Hardware:
    DEV = None

    def __init__(self, pin, hardware):
        if hardware == 'Relay':
            self.DEV = Relay(pin)
        elif hardware == 'Mock':
            self.DEV = HardwareMock(pin)
        else:
            raise Exception("Hardware not yet implemented")

    def get_state(self):
        return self.DEV.get_state()


class Relay(Hardware):
    def __init__(self, pin):
        self.DEV = gpiozero.OutputDevice(pin, active_high=True)

    def switch_off(self):
        self.DEV.on()

    def switch_on(self):
        self.DEV.off()

    def toggle(self):
        self.DEV.toggle()

    def get_state(self):
        return self.DEV.value


class HardwareMock(Hardware):
    state = False

    def __init__(self, pin):
        pass

    def get_state(self):
        return self.state

    def toggle(self):
        self.state = not self.state

    def set(self, state):
        self.state = state
