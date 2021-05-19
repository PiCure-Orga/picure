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

    sensor = escape(sensor)
    minutes = escape(minutes)

    sensors = " ".join('"{}",'.format(i) for i in sensor.split(","))[:-1]
    minutes = int(minutes)

    if minutes > 10:
        db_name = "latest_30_days"
    elif 0 < minutes <= 10:
        db_name = "latest_10_minutes"
        minutes = minutes * 6
    else:
        abort(500, "Valid minutes must not exceed integer range or be negative")

    # I fully understand that this is not a good idea. However passing the comma separated list of sensors
    # escapes the required quotes and commas. There is escaping done above so this should be fine...
    cmd = "SELECT timestamp, sensor, value from {} where sensor in ({}) order by id desc limit {}".format(
        db_name, sensors, minutes
    )

    result = db.cursor().execute(cmd).fetchall()

    res = [(d["timestamp"], d["sensor"], d["value"]) for d in result]
    return json.dumps(res)


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
