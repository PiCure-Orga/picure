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
import json
from flask import Blueprint, request
from picure.Backend.Program import controler
from picure.Backend.DB.db_handler import get_db

program = Blueprint("program", __name__, template_folder="templates")


@program.route("/api/program", methods=["GET"])
def get_programs():
    progs = [{"id": t.program_id, "name": t.name, "steps": len(t.get_steps())} for t in
             controler.get_list_of_programs()]
    return json.dumps(progs)


@program.route("/api/program", methods=["POST"])
def new_program():
    form_data = request.form.to_dict()
    if "program_name" in form_data:
        get_db().cursor().execute("INSERT INTO program (name) VALUES (:program_name)", form_data )
        get_db().commit()
        get_db().cursor().close()
    return get_programs()