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
from datetime import datetime
import time
from picure.Backend.Scheduler import Scheduler
from picure.Backend.hardware_controller import get_hardware
from picure.Backend.action_task import ActionTask


class Task:
    id = None
    name = None
    hardware = None
    action = None
    duration = None

    def __init__(self, id, name, hardware, action, duration):
        self.id = id
        self.name = name
        self.hardware = get_hardware(hardware)
        self.action = ActionTask(action)
        self.duration = duration

    def exec(self):
        self.hardware.execute(self.action)
        if self.duration != 0:
            scheduler = Scheduler()
            if not self.name in [f.id for f in scheduler.get_jobs()]:
                scheduler.add_job(
                    func=self.handle_duration,
                    trigger="date",
                    run_date=datetime.fromtimestamp(time.time() + self.duration),
                    id=self.name,
                )

    def handle_duration(self):
        if self.action == ActionTask.SWITCH_OFF:
            self.hardware.on()
        elif self.action == ActionTask.TOGGLE:
            self.action.toggle()
        else:
            self.hardware.off()
