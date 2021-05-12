import time

from core.DB import db_handler
from . import scheduler
from core.Backend.hardware_controller import get_all_sensor_data


@scheduler.task(
    "interval",
    id="every_ten_seconds",
    seconds=10,
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def log_every_ten_seconds():
    to_write = []
    for data in get_all_sensor_data().items():
        to_write.append((time.time(), data[0], data[1]))

    with scheduler.app.app_context():
        db = db_handler.get_db()
        db.cursor().executemany(
            "insert into latest_10_minutes (timestamp, sensor, value) values (?, ?, ?)",
            to_write,
        )
        db.cursor().execute(
            "DELETE FROM latest_10_minutes where id < "
            "(SELECT MIN(id) from ("
            "select id from latest_10_minutes order by id desc limit 100))"
        )
        db.commit()
        db.cursor().close()


@scheduler.task(
    "interval",
    id="every_minute",
    seconds=5,
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def calculate_minute_avg():
    with scheduler.app.app_context():
        db = db_handler.get_db()
        result = (
            db.cursor()
            .execute(
                "select sensor, avg(value) as avg from latest_10_minutes group by sensor"
            )
            .fetchall()
        )
        db.cursor().close()

        for s in result:
            print(s["sensor"] + " AVG: " + str(s["avg"]))
