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
import time

from picure.DB.db_handler import get_db
from picure.Backend.Program.event import Event
from datetime import datetime


class Program:
    run_id = None
    program_id = None
    name = None
    targets = []
    events = []

    def __init__(self, prog_id, run_id, name):
        self.program_id = prog_id
        self.run_id = run_id
        self.name = name

    def get_events(self):
        if len(self.events == 0):
            fetched = (
                get_db()
                .cursor()
                .execute(
                    "SELECT id,sensor,eval,derivation from event where program_id = ?",
                    self.program_id,
                )
                .fetchall()
            )
            for f in fetched:
                self.events.append(
                    Event(f["id"], f["sensor"], f["eval"], f["derivation"])
                )
            get_db().cursor().close()

        return self.events

    def get_step_targets(self):
        if len(self.targets == 0):
            fetched = (
                get_db()
                .cursor()
                .execute(
                    "SELECT * FROM step where program_id = ? order by step_order desc",
                    self.program_id,
                )
                .fetchall()
            )
            for f in fetched:
                fetch = (
                    get_db()
                    .cursor()
                    .execute("SELECT * FROM target where step_id = ?", f["id"])
                    .fetchall()
                )
                targets = {t["sensor"]: t["value"] for t in targets}
                self.targets.append((f["duration"], targets))

        return self.targets

    def get_current_step(self):
        start = (
            get_db()
            .cursor()
            .execute(
                "SELECT start_timestamp from program_run where id = ?", self.run_id
            )
            .fetchall()["start_timestamp"]
        )
        passed = time.time() - start

        step_time_in = 0
        step = 0

        for t in self.get_step_targets():
            if step_time_in <= passed:
                step_time_in += t[1]
                step += 1
            else:
                break

        return self.targets.index(step - 1)
