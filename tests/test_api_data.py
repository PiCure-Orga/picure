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

from picure.DB.db_handler import get_db


def test_api_data(client, app):
    with app.app_context():

        get_db().cursor().execute(
            "INSERT INTO latest_30_days (timestamp, sensor, value) VALUES (?,?,?)",
            (123, "SENSOR_TEMP", 100)
        )
        get_db().commit()
        get_db().cursor().close()

        result = get_db().cursor().execute("SELECT * FROM latest_30_days").fetchall()
        get_db().cursor().close()

    assert client.get("/data/SENSOR_TEMP/1").data == b'[]'
    assert client.get("/data/SENSOR_TEMP/10").data == b'[]'
    assert client.get("/data/SENSOR_TEMP/11").data == b'[[123, "SENSOR_TEMP", 100]]'

