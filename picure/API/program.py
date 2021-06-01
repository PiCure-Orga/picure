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
import sqlite3

from flask import Blueprint, request, Response, abort
from picure.Backend.Program import controler
from picure.Backend.DB.db_handler import get_db

program = Blueprint("program", __name__, template_folder="templates")


@program.route("/api/program", methods=["GET"])
def get_programs():
    progs = [
        {"id": t[1].program_id, "name": t[1].name, "steps": len(t[1].get_steps())}
        for t in controler.get_dict_of_programs()
    ]
    return json.dumps(progs)


@program.route("/api/program", methods=["POST"])
def new_program():
    form_data = request.form.to_dict()
    if "ProgramName" in form_data:
        db = get_db()
        db.cursor().execute(
            "INSERT INTO program (name) VALUES (:ProgramName)", form_data
        )
        db.commit()
        db.cursor().close()
    return Response(response="No Content", status=204)


@program.route("/api/program/<string:prog_id>", methods=["DELETE"])
def delete_program(prog_id):
    db = get_db()
    if (
        db.cursor()
        .execute(
            "SELECT max(enabled) as enabled from program_run where program_id = ?", (prog_id,)
        )
        .fetchone()['enabled']
        == 1
    ):
        abort(500, "Cant delete currently running program")
    db.cursor().execute("DELETE from program where id = ?", (prog_id,))
    db.commit()
    db.cursor().close()
    return "Ok"

@program.route("/api/program/<int:prog_id>", methods=['GET'])
def get_program(prog_id):
    programs = controler.get_dict_of_programs()
    if prog_id not in programs:
        abort(500, "Program not found")

    steps = programs[prog_id].get_step_targets()
    return json.dumps(steps)