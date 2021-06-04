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
from flask import Blueprint, request, Response, abort
from picure.Backend.Program import controler
from picure.Backend.DB.db_handler import get_db

program = Blueprint("program", __name__, template_folder="templates")


@program.route("/api/program", methods=["GET"])
def get_programs():
    return json.dumps(
        [
            {"program_id": p[1].program_id, "program_name": p[1].name}
            for p in controler.get_dict_of_programs().items()
        ]
    )


@program.route("/api/program", methods=["POST"])
def new_program():
    form_data = request.form.to_dict()
    if "ProgramName" in form_data and len(form_data) == 1:
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
            "SELECT max(enabled) as enabled from program_run where program_id = ?",
            (prog_id,),
        )
        .fetchone()["enabled"]
        == 1
    ):
        abort(500, "Cant delete currently running program")
    db.cursor().execute("DELETE from program where id = ?", (prog_id,))
    db.commit()
    db.cursor().close()
    return Response(status=204, response="Deleted program")


@program.route("/api/program/<int:prog_id>", methods=["GET"])
def get_program(prog_id):
    programs = controler.get_dict_of_programs()
    if prog_id not in programs:
        abort(500, "Program not found")

    steps = programs[prog_id].get_step_targets()
    return json.dumps(steps)


@program.route("/api/program/<int:prog_id>/step", methods=["POST"])
def add_step(prog_id):
    form = request.form.to_dict()
    if not ("value" in form and "unit" in form and len(form) == 2):
        abort(500, "Malformed request")

    if form["unit"] == "s":
        converted_duration = int(form["value"]) * 1000
    elif form["unit"] == "m":
        converted_duration = int(form["value"]) * 1000 * 60
    elif form["unit"] == "h":
        converted_duration = int(form["value"]) * 1000 * 60 * 60
    elif form["unit"] == "d":
        converted_duration = int(form["value"]) * 1000 * 60 * 60 * 24

    get_db().cursor().execute(
        "INSERT INTO step (program_id, duration, step_order) VALUES (:prog_id, :duration , (SELECT max(step_order) FROM step where program_id = :prog_id)+1 )",
        {"prog_id": prog_id, "duration": converted_duration},
    )
    get_db().commit()
    get_db().cursor().close()

    return Response(response="No content", status=204)


@program.route("/api/program/<int:prog_id>/step/<int:step_id>", methods=["DELETE"])
def delete_step(prog_id, step_id):
    get_db().cursor().execute(
        "DELETE from step where program_id = :prog_id and step_order = :step_id",
        {"prog_id": prog_id, "step_id": step_id},
    )
    get_db().commit()
    get_db().cursor().close()
    return Response(
        response="Deleted step " + str(step_id) + "from program " + str(prog_id),
        status=204,
    )


@program.route("/api/program/<int:prog_id>/step/<int:step_id>/target", methods=["GET"])
def get_steps(prog_id, step_id):
    targets = controler.get_dict_of_programs()[prog_id].get_step_targets()
    target = [t for t in targets if t[0] == step_id][0]

    return json.dumps(target[2])


@program.route("/api/program/<int:prog_id>/step/<int:step_id>/target", methods=["POST"])
def new_step(prog_id, step_id):
    form = request.form.to_dict()
    if not ("sensor" in form and "value" in form and len(form) == 2):
        abort(500, "Malformed request")

    allready_present = (
        get_db()
        .cursor()
        .execute(
            "SELECT sum(id) as count FROM target where step_id = :step_id and sensor = :sensor",
            {"step_id": step_id, "sensor": form["sensor"].upper()},
        )
        .fetchone()["count"]
    )
    if allready_present:
        abort(500, "Sensor cant have multiple targets at once")

    get_db().cursor().execute(
        "INSERT INTO target (step_id, sensor, value) VALUES (:step_id, :sensor, :value)",
        {"step_id": step_id, "sensor": form["sensor"], "value": form["value"]},
    )

    get_db().commit()
    get_db().cursor().close()

    return Response(response="Target created", status=204)


@program.route(
    "/api/program/<int:prog_id>/step/<int:step_id>/target/<sensor>", methods=["DELETE"]
)
def delete_target(prog_id, step_id, sensor):
    get_db().cursor().execute(
        "DELETE from target where step_id = :step_id and sensor = :sensor",
        {"step_id": step_id, "sensor": sensor},
    )
    get_db().commit()
    get_db().cursor().close()

    return Response(response="Deleted step", status=204)


@program.route("/api/program/<int:prog_id>/event", methods=["POST"])
def new_prog_event(prog_id):
    form = request.form.to_dict()
    if not (
        "name" in form
        and "sensor" in form
        and "eval" in form
        and "derivation" in form
        and len(form) == 4
    ):
        abort(500)

    get_db().cursor().execute(
        "INSERT INTO event (program_id, name, sensor, eval, derivation) VALUES (?,?,?,?,?)",
        (prog_id, form["name"], form["sensor"], form["eval"], form["derivation"]),
    )
    get_db().commit()
    get_db().cursor().close()

    return Response(response="Event created", status=204)


@program.route("/api/program/<int:prog_id>/event", methods=["GET"])
def get_prog_events(prog_id):
    dat = (
        get_db()
        .cursor()
        .execute(
            "SELECT id,name,sensor,eval,derivation from event where program_id = ?",
            (prog_id,),
        )
        .fetchall()
    )
    return json.dumps(
        [
            {
                "id": r["id"],
                "name": r["name"],
                "sensor": r["sensor"],
                "evaluation": r["eval"],
                "derivation": r["derivation"],
            }
            for r in dat
        ]
    )


@program.route("/api/program/<int:prog_id>/event/<int:event_id>", methods=["DELETE"])
def delete_event(prog_id, event_id):
    get_db().cursor().execute("DELETE FROM event where id=?", (event_id,))
    get_db().commit()
    get_db().cursor().close()
    return Response(response="Event deleted", status=204)


@program.route("/api/program/<int:prog_id>/event/<int:event_id>/task", methods=["POST"])
def new_event_tasks(prog_id, event_id):
    form = request.form.to_dict()
    if not (
        "name" in form
        and "hardware" in form
        and "action" in form
        and "duration" in form
        and len(form) == 4
    ):
        abort(500)

    get_db().cursor().execute(
        "INSERT INTO task (event_id, name, hardware, action, duration) VALUES (?,?,?,?,?)",
        (event_id, form["name"], form["hardware"], form["action"], form["duration"]),
    )
    get_db().commit()
    get_db().cursor().close()
    return Response(response="Task created", status=204)


@program.route("/api/program/<int:prog_id>/event/<int:event_id>/task", methods=["GET"])
def get_event_tasks(prog_id, event_id):
    dat = (
        get_db()
        .cursor()
        .execute(
            "SELECT id, name, hardware, action, duration FROM task where event_id = ?",
            (event_id,),
        )
        .fetchall()
    )
    return json.dumps(
        [
            {
                "id": r["id"],
                "name": r["name"],
                "hardware": r["hardware"],
                "action": r["action"],
                "duration": r["duration"],
            }
            for r in dat
        ]
    )


@program.route(
    "/api/program/<int:prog_id>/event/<int:event_id>/task/<int:task_id>",
    methods=["DELETE"],
)
def delete_event_tasks(prog_id, event_id, task_id):
    get_db().cursor().execute("DELETE FROM task where id = ?", (task_id,))
    get_db().commit()
    get_db().cursor().close()
    return Response(response="Task deleted", status=204)
