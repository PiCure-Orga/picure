from flask import Blueprint, abort, request, escape
from core.DB import db_handler
import json

loggerio = Blueprint("loggerio", __name__, template_folder="templates")


@loggerio.route("/data/<sensor>/<minutes>", methods=["GET"])
def get_sensor_data(minutes, sensor):
    db = db_handler.get_db()

    sensor = escape(sensor)
    minutes = escape(minutes)

    sensors = " ".join('"{}",'.format(i) for i in sensor.split(","))
    minutes = int(minutes)

    if minutes > 10:
        db_name = "latest_30_days"
    elif 0 < minutes <= 10:
        db_name = "latest_10_minutes"
    else:
        abort(500, "Valid minutes must not exceed integer range or be negative")

    # I fully understand that this is not a good idea. However passing the comma separated list of sensors
    # escapes the required quotes and commas. There is escaping done above so this should be fine...
    cmd = "SELECT timestamp, sensor, value from {} where sensor in ({}) order by id desc limit {}".format(
        db_name, sensors[:-1], minutes
    )

    result = db.cursor().execute(cmd).fetchall()

    res = [(d["timestamp"], d["sensor"], d["value"]) for d in result]
    return json.dumps(res)


@loggerio.route("/data/<sensor>", methods=["POST"])
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
