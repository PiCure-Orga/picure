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
from picure.DB import db_handler


def test_connection(app):
    with app.app_context():
        assert db_handler.get_db() is not None


def test_insert(app):
    with app.app_context():
        db_handler.get_db().cursor().execute(
            "INSERT into latest_30_days (timestamp, sensor, value) VALUES (?,?,?)",
            (100, "TEST", 1337),
        )
        db_handler.get_db().commit()
        db_handler.get_db().cursor().close()

        result = (
            db_handler.get_db()
            .cursor()
            .execute("SELECT timestamp,sensor,value FROM latest_30_days")
            .fetchall()
        )
        db_handler.get_db().cursor().close()

        assert result[0]["timestamp"] == 100
        assert result[0]["sensor"] == "TEST"
        assert result[0]["value"] == 1337
        assert len(result) == 1
