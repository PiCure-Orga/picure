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
from abc import ABC, abstractmethod

from picure.Backend.action_task import ActionTask
from picure.Backend.io.prototypes.base import Base


class HardwareProto(Base, ABC):
    DEV = None

    @abstractmethod
    def __init__(self, pin, name):
        pass

    def execute(self, task: ActionTask):
        if task == ActionTask.TOGGLE:
            self.toggle()
        elif task == ActionTask.SWITCH_ON:
            self.on()
        elif task == ActionTask.SWITCH_OFF:
            self.off()
        else:
            raise Exception("Action not supported by this hardware!")

    @abstractmethod
    def on(self):
        pass

    @abstractmethod
    def off(self):
        pass

    @abstractmethod
    def toggle(self):
        pass
