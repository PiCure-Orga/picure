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

from picure.Backend.DB.db_handler import get_db


def test_api_run(client, program, app):
    assert len(json.loads(client.get("/api/run").data)) == 1
    assert json.loads(client.get("/api/run").data)[0]["id"] == 1
    with app.app_context():
        assert (
            get_db()
            .cursor()
            .execute("SELECT count(id) as count FROM program_run")
            .fetchone()["count"]
            == 1
        )

    assert (
        client.post("/api/run", data=dict(program_id=1, enabled=1)).status
        == "204 NO CONTENT"
    )
    assert len(json.loads(client.get("/api/run").data)) == 2
    with app.app_context():
        assert (
            get_db()
            .cursor()
            .execute("SELECT count(id) as count FROM program_run")
            .fetchone()["count"]
            == 2
        )

    assert client.delete("/api/run/2").status == "204 NO CONTENT"
    assert len(json.loads(client.get("/api/run").data)) == 1
    with app.app_context():
        assert (
            get_db()
            .cursor()
            .execute("SELECT count(id) as count FROM program_run")
            .fetchone()["count"]
            == 1
        )

    assert (
        client.patch("/api/run/1", data=dict(enabled=True)).status == "204 NO CONTENT"
    )
    assert json.loads(client.get("/api/run").data)[0]["enabled"] == 1
    with app.app_context():
        assert (
            get_db()
            .cursor()
            .execute("SELECT enabled FROM program_run where program_id = 1")
            .fetchone()["enabled"]
            == 1
        )
