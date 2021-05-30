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
from picure.Backend.DB.db_handler import get_db
from picure.Backend.Program import controler
from picure.Backend.io.hardware import HardwareMock


def test_program(app, program):
    with app.app_context():
        assert program.program_id == 1
        assert len(program.get_events()) == 1
        assert program.name == "TEST"

        assert (program.get_step_targets()[0][1])["SENSOR_TEMP"] == 100
        assert (program.get_step_targets()[0][1])["SENSOR_HUMID"] == 100

        for e in program.get_events():
            assert len(e.get_tasks()) == 1
            for t in e.get_tasks():
                assert isinstance(t.hardware, HardwareMock)
            e.check()
            assert len(Scheduler().get_jobs()) == 1


def test_sanity_check(app, program):
    with app.app_context():
        get_db().cursor().execute(
            "INSERT INTO program_run (program_id, enabled) VALUES (1, 1)"
        )
        assert controler.get_current_program() == 0
        assert controler.sanity_checks() == True
