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

from picure.Backend.DB.db_handler import get_db
from picure.Backend.Program.event import Event


class Program:
    run_id = None
    program_id = None
    name = None

    def __init__(self, prog_id, run_id, name):
        self.program_id = prog_id
        self.run_id = run_id
        self.name = name

    def get_events(self):
        events = []
        fetched = (
            get_db()
            .cursor()
            .execute(
                "SELECT id, sensor, eval, derivation from event where program_id = ?",
                (self.program_id,),
            )
            .fetchall()
        )
        for f in fetched:
            events.append(Event(f["id"], f["sensor"], f["eval"], f["derivation"], self))
        get_db().cursor().close()

        return events

    def get_steps(self):
        return (
            get_db()
            .cursor()
            .execute(
                "SELECT id, duration FROM step where program_id = ? order by step_order asc",
                (self.program_id,),
            )
            .fetchall()
        )

    def get_step_targets(self):
        to_return = []
        steps = self.get_steps()

        for s in steps:
            db_targets = (
                get_db()
                .cursor()
                .execute(
                    "SELECT sensor, value FROM target where step_id = ?",
                    (s["id"],),
                )
                .fetchall()
            )
            targets = {t["sensor"]: t["value"] for t in db_targets}
            to_return.append((s["id"], s["duration"], targets))

        return to_return

    def get_current_targets(self):
        if self.run_id == 0:
            return None
        start = (
            get_db()
            .cursor()
            .execute(
                "SELECT start_timestamp from program_run where id = ?",
                (self.run_id,),
            )
            .fetchall()
        )
        passed = time.time() - start[0]["start_timestamp"]

        step_time_in = 0
        step = 0

        for t in self.get_step_targets():
            if step_time_in <= passed:
                step_time_in += t[1]
                step += 1

        return self.get_step_targets()[step - 1][2]
