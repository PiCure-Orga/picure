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

from flask import Blueprint, request, abort, Response
from picure.Backend.DB.db_handler import get_db

run = Blueprint("run", __name__, template_folder="templates")


@run.route("/api/run", methods=["GET"])
def get_run():
    runs = (
        get_db()
        .cursor()
        .execute(
            "SELECT pr.id as id, pr.program_id as program_id, pr.enabled as enabled, pr.start_timestamp as start_timestamp, p.name as name FROM program_run pr join program p on pr.program_id = p.id"
        )
        .fetchall()
    )
    return json.dumps(
        [
            {
                "id": r["id"],
                "program_id": r["program_id"],
                "name": r["name"],
                "enabled": r["enabled"],
                "start_timestamp": r["start_timestamp"],
            }
            for r in runs
        ]
    )


@run.route("/api/run/<int:run_id>", methods=["DELETE"])
def delete_run(run_id):
    get_db().cursor().execute("DELETE FROM program_run where id=?", (run_id,))
    get_db().commit()
    get_db().cursor().close()
    return Response(response="Deleted program run", status=204)


@run.route("/api/run", methods=["POST"])
def add_run():
    form = request.form.to_dict()
    if not ("program_id" in form and "enabled" in form):
        abort(500)

    enabled = 1 if form["enabled"].lower() == "true" else 0

    get_db().cursor().execute("UPDATE program_run SET enabled = 0")
    get_db().cursor().execute(
        "INSERT INTO program_run (program_id, enabled, start_timestamp ) values (?,?, (SELECT strftime('%s','now')) )",
        (form["program_id"], enabled),
    )
    get_db().commit()
    get_db().cursor().close()

    return Response(response="Program run started", status=204)


@run.route("/api/run/<int:run_id>", methods=["PATCH"])
def patch_run(run_id):
    form = request.form.to_dict()
    if not ("enabled" in form and len(form) == 1):
        abort(500)

    enabled = 1 if form["enabled"].lower() == "true" else 0

    get_db().cursor().execute(
        "UPDATE program_run SET enabled=:enabled where id=:run_id",
        {"enabled": enabled, "run_id": run_id},
    )
    get_db().commit()
    get_db().cursor().close()
    return Response(response="Program updated", status=204)
