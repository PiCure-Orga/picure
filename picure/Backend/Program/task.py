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
from picure.Backend.hardware_controller import get_hardware
from picure.Backend.action_task import ActionTask
from flask_apscheduler.scheduler import APScheduler
from time import time
from datetime import datetime


class Task:
    id = None
    name = None
    hardware = None
    action = None
    duration = None

    def __init__(self, id, name, hardware, action, duration):
        self.id = id
        self.name = name
        self.hardware = get_hardware(hardware)[1]
        self.action = ActionTask(action)
        self.duration = duration

    def exec(self):
        self.hardware.execute(self.action)
        if self.duration != 0:
            APScheduler.add_job(
                self.handle_duration,
                "date",
                datetime.fromtimestamp(time.time() + self.duration),
            )

    def handle_duration(self):
        if self.action == ActionTask.SWITCH_OFF:
            self.hardware.on()
        else:
            self.hardware.off()
