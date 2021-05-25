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
from picure.DB.db_handler import get_db
from picure.Backend.Program.event import Event


class Program:
    db_id = None
    name = None
    events = []

    def __init__(self, id, name):
        self.db_id = id
        self.name = name

    def get_events(self):
        if len(self.events == 0):
            fetched = (
                get_db()
                .cursor()
                .execute(
                    "SELECT id,sensor,eval,derivation from event where program_id = ?",
                    self.db_id,
                )
                .fetchall()
            )
            for f in fetched:
                self.events.append(
                    Event(f["id"], f["sensor"], f["eval"], f["derivation"])
                )
            get_db().cursor().close()

        return self.events
