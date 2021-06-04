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


def test_api_program(client, program, app):
    json_data = json.loads(client.get("/api/program").data)
    assert json_data[0]["program_id"] == 1
    with app.app_context():
        assert (
            len(get_db().cursor().execute("SELECT count(id) FROM program").fetchone())
            == 1
        )

    assert (
        client.post("/api/program", data=dict(ProgramName="Pytest")).status
        == "204 NO CONTENT"
    )
    with app.app_context():
        assert (
            get_db()
            .cursor()
            .execute("SELECT count(id) as count FROM program")
            .fetchone()["count"]
            == 2
        )

    assert client.delete("/api/program/2").status == "204 NO CONTENT"
    with app.app_context():
        assert (
            get_db()
            .cursor()
            .execute("SELECT count(id) as count FROM program")
            .fetchone()["count"]
            == 1
        )

    assert json.loads(client.get("/api/program/1").data)[0][2]["SENSOR_HUMID"] == 100

    with app.app_context():
        assert (
            get_db()
            .cursor()
            .execute("SELECT count(id) as count from step where program_id = 1")
            .fetchone()["count"]
            == 1
        )

    assert (
        client.post("/api/program/1/step", data=dict(value=1, unit="s")).status
        == "204 NO CONTENT"
    )
    assert (
        client.post("/api/program/1/step", data=dict(value=1, unit="m")).status
        == "204 NO CONTENT"
    )
    assert (
        client.post("/api/program/1/step", data=dict(value=1, unit="h")).status
        == "204 NO CONTENT"
    )
    assert (
        client.post("/api/program/1/step", data=dict(value=1, unit="d")).status
        == "204 NO CONTENT"
    )
    with app.app_context():
        assert (
            get_db()
            .cursor()
            .execute(
                "SELECT duration FROM step where program_id = 1 and step_order = 2"
            )
            .fetchone()["duration"]
            == 1000
        )
        assert (
            get_db()
            .cursor()
            .execute(
                "SELECT duration FROM step where program_id = 1 and step_order = 3"
            )
            .fetchone()["duration"]
            == 60000
        )
        assert (
            get_db()
            .cursor()
            .execute(
                "SELECT duration FROM step where program_id = 1 and step_order = 4"
            )
            .fetchone()["duration"]
            == 3600000
        )
        assert (
            get_db()
            .cursor()
            .execute(
                "SELECT duration FROM step where program_id = 1 and step_order = 5"
            )
            .fetchone()["duration"]
            == 86400000
        )

    assert client.delete("/api/program/1/step/2").status == "204 NO CONTENT"
    with app.app_context():
        assert (
            get_db()
            .cursor()
            .execute("SELECT count(id) as count from step where program_id = 1")
            .fetchone()["count"]
            == 4
        )

    assert (
        json.loads(client.get("/api/program/1/step/1/target").data)["SENSOR_TEMP"]
        == 100
    )
    assert (
        json.loads(client.get("/api/program/1/step/1/target").data)["SENSOR_HUMID"]
        == 100
    )

    assert (
        client.post(
            "/api/program/1/step/1/target", data=dict(sensor="TEST", value=100)
        ).status
        == "204 NO CONTENT"
    )
    assert json.loads(client.get("/api/program/1/step/1/target").data)["TEST"] == 100

    with app.app_context():
        assert (
            get_db()
            .cursor()
            .execute("SELECT count(id) as count from target where step_id = 1")
            .fetchone()["count"]
            == 3
        )

    assert client.delete("/api/program/1/step/1/target/TEST").status == "204 NO CONTENT"
    with app.app_context():
        assert (
            get_db()
            .cursor()
            .execute("SELECT count(id) as count from target where step_id = 1")
            .fetchone()["count"]
            == 2
        )

    assert (
        json.loads(client.get("/api/program/1/event").data)[0]["name"]
        == "TEMP < TARGET -2"
    )

    assert len(json.loads(client.get("/api/program/1/event/1/task").data)) == 1
    with app.app_context():
        assert (
            get_db()
            .cursor()
            .execute("SELECT count(id) as count from task where event_id = 1")
            .fetchone()["count"]
            == 1
        )

    assert (
        client.post(
            "/api/program/1/event/1/task",
            data=dict(name="TEST", hardware="TEST_HW", action=1, duration=0),
        ).status
        == "204 NO CONTENT"
    )
    assert len(json.loads(client.get("/api/program/1/event/1/task").data)) == 2
    with app.app_context():
        assert (
            get_db()
            .cursor()
            .execute("SELECT count(id) as count from task where event_id = 1")
            .fetchone()["count"]
            == 2
        )

    assert client.delete("/api/program/1/event/1/task/2").status == "204 NO CONTENT"
    assert len(json.loads(client.get("/api/program/1/event/1/task").data)) == 1
    with app.app_context():
        assert (
            get_db()
            .cursor()
            .execute("SELECT count(id) as count from task where event_id = 1")
            .fetchone()["count"]
            == 1
        )

    assert (
        client.post(
            "/api/program/1/event",
            data=dict(name="TEST", sensor="TEST", eval="=", derivation="2"),
        ).status
        == "204 NO CONTENT"
    )
    assert len(json.loads(client.get("/api/program/1/event").data)) == 2
    assert client.delete("/api/program/1/event/2").status == "204 NO CONTENT"
    assert len(json.loads(client.get("/api/program/1/event").data)) == 1
