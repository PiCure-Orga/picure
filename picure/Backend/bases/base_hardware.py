#      PiCure - Meat dry ageing and curing
#      Copyright (C) <2021>  <Markus Hupfauer>
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

import gpiozero


class Hardware:
    DEV = None

    def __init__(self, pin, hardware):
        if hardware == "Relay":
            self.DEV = Relay(pin)
        elif hardware == "Mock":
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
