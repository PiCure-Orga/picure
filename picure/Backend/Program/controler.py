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
from picure.Backend.Program.program import Program


def sanity_checks():
    if len(
        get_db()
        .cursor()
        .execute("SELECT id FROM program_run where enabled = 1")
        .fetchall()
        > 1
    ):
        get_db().cursor().execute(
            "UPDATE program_run SET enabled = 0 where enabled = 1"
        )
        get_db().commit()
        get_db().cursor().close()
        raise Exception("No more than one program can be enabled at a time!")


def get_current_program():
    sanity_checks()
    res = (
        get_db()
        .cursor()
        .execute(
            "SELECT id,name from program p join program_run pr on p.id = pr.program_id where pr.enabled = 1"
        )
        .fetchall()
    )
    get_db().cursor().close()
    return Program(res["id"], res["name"])
