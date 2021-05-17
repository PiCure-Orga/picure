from flask import Blueprint, abort, request
from core.DB import db_handler
import json

loggerio = Blueprint("loggerio", __name__, template_folder="templates")


@loggerio.route("/data/<minutes>/<sensor>", methods=["GET"])
def get_sensor_data(minutes, sensor):
    db = db_handler.get_db()
    result = None

    minutes = int(minutes)

    if minutes > 10:
        result = (
            db.cursor()
            .execute(
                "SELECT timestamp, sensor, value from latest_30_days where sensor in (?) order by id desc limit ?",
                (sensor, minutes),
            )
            .fetchall()
        )

    elif 0 < minutes <= 10:
        result = (
            db.cursor()
            .execute(
                "SELECT timestamp, sensor, value from latest_10_minutes where sensor in (?) order by id desc limit ?",
                (sensor, minutes * 6),
            )
            .fetchall()
        )

    else:
        abort(500, "Valid minutes must not exceed integer range or be negative")

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
