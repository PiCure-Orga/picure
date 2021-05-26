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
from picure.Backend.DB.db_handler import get_db
from picure.Backend.Program.task import Task


class Event:
    db_id = None
    program = None
    sensor = None
    evaluation = None
    derivation = None
    target = None
    tasks = []

    def __init__(self, id, sensor, evaluation, derivation, program):
        self.db_id = id
        self.sensor = get_hardware(sensor)
        self.evaluation = evaluation
        self.derivation = derivation
        self.program = program
        self.target = program.get_current_targets().get(self.sensor.name) or None


    def check(self):
        expr = (
            str(self.sensor)
            + str(self.evaluation)
            + "("
            + str(self.target)
            + "+"
            + str(self.derivation)
            + ")"
        )
        to_exec = eval(expr)

        if to_exec:
            for t in self.get_tasks():
                t.exec()

    def get_tasks(self):
        if len(self.tasks) == 0:
            fetched = (
                get_db()
                .cursor()
                .execute(
                    "SELECT id,name,hardware,action,duration from task where event_id = ?",
                    self.db_id,
                )
                .fetchall()
            )
            for f in fetched:
                self.tasks.append(
                    Task(f["id"], f["name"], f["hardware"], f["action"], f["duration"])
                )

        return self.tasks
