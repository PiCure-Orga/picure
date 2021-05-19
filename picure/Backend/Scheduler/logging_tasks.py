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

import time

from picure.DB import db_handler
from . import scheduler
from picure.Backend.hardware_controller import get_all_sensor_data


@scheduler.task(
    "interval",
    id="every_ten_seconds",
    seconds=10,
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def log_every_ten_seconds():
    to_write = [
        (time.time(), data[0], data[1]) for data in get_all_sensor_data().items()
    ]

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
    minutes=1,
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def calculate_minute_avg():
    with scheduler.app.app_context():
        db = db_handler.get_db()
        # Get latest 6 sensor entries and average them (All 10 seconds one data-point * 6 = 60 seconds covered)
        result = (
            db.cursor()
            .execute(
                "select sensor, avg(value) as avg from ("
                "select sensor, value from latest_10_minutes "
                "order by id desc limit 6) group by sensor"
            )
            .fetchall()
        )
        db.cursor().close()

        to_write = [(time.time(), d["sensor"], d["avg"]) for d in result]

        db = db_handler.get_db()
        db.cursor().execute(
            "DELETE FROM latest_30_days where id < "
            "(SELECT MIN(id) from ("
            "select id from latest_30_days order by id desc limit 43200))"
        )
        db.commit()
        db.cursor().close()

        db = db_handler.get_db()
        db.cursor().executemany(
            "insert into latest_30_days (timestamp, sensor, value) VALUES (?,?,?)",
            to_write,
        )
        db.commit()
        db.cursor().close()
