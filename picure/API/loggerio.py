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

from flask import Blueprint, abort, request, escape
from markupsafe import escape
from picure.DB import db_handler
import json

loggerio = Blueprint("loggerio", __name__, template_folder="templates")


@loggerio.route("/data/<string:sensor>/<int:minutes>", methods=["GET"])
def get_sensor_data(minutes, sensor):
    db = db_handler.get_db()

    sensor = sensor.split(",")
    minutes = minutes

    minutes = minutes

    if minutes > 10:
        db_name = "latest_30_days"
    elif 0 < minutes <= 10:
        db_name = "latest_10_minutes"
        minutes = minutes * 6
    else:
        abort(500, "Valid minutes must not exceed integer range or be negative")

    result = [
        (
            db.cursor()
            .execute(
                "SELECT timestamp, sensor, value from {} where sensor in (?) order by id desc limit ?".format(
                    db_name
                ),
                (s, minutes),
            )
            .fetchall()
        )
        for s in sensor
    ]

    to_return = []

    for res in result:
        for row in res:
            to_return.append((row["timestamp"], row["sensor"], row["value"]))

    return json.dumps(to_return)


@loggerio.route("/data/<string:sensor>", methods=["POST"])
def insert_sensor_data(sensor):
    to_insert = request.form.to_dict()

    if len(to_insert) != 2:
        abort(500, "Too many arguments")

    if any(k not in to_insert.keys() for k in ("value", "timestamp")):
        abort(500, "Only pass value and timestamp")

    db = db_handler.get_db()
    db.cursor().execute(
        "INSERT INTO latest_30_days (timestamp, sensor, value) VALUES (?, ?, ?)",
        (to_insert["timestamp"], sensor, to_insert["value"]),
    )
    db.commit()
    db.cursor().close()

    return "OK"
