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

from picure.Backend.DB.db_handler import get_db
from picure.Backend.Program.program import Program


def sanity_checks():
    res = (
        get_db()
        .cursor()
        .execute("SELECT id FROM program_run where enabled = 1")
        .fetchall()
    )

    if len(res) > 1:
        get_db().cursor().execute(
            "UPDATE program_run SET enabled = 0 where enabled = 1"
        )
        get_db().commit()
        get_db().cursor().close()
        return False
    return True


def get_list_of_programs():
    if not sanity_checks():
        return 0

    res = get_db().cursor().execute("SELECT id,name from program").fetchall()
    return [Program(r["id"], 0, r["name"]) for r in res]


def get_current_program():
    if not sanity_checks():
        return 0

    res = (
        get_db()
        .cursor()
        .execute(
            "SELECT p.id,pr.id,p.name from program p join program_run pr on p.id = pr.program_id where pr.enabled = 1"
        )
        .fetchall()
    )
    get_db().cursor().close()
    if len(res) == 0:
        raise Exception(
            "Tried to get current program when no program is running. Enable a program."
        )
    return Program(res[0][0], res[0][1], res[0][2])
