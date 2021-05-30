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
from picure.Backend.Scheduler import Scheduler
from picure.Backend.Program import controler

scheduler = Scheduler()


@scheduler.task(
    "interval",
    id="Program_Event_Loop",
    seconds=10,
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def validate_events():
    with scheduler.app.app_context():
        events = controler.get_current_program().get_events()
        for e in events:
            e.check()
