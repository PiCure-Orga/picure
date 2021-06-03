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


def test_state_control_get(client):
    assert client.get("/api/state/HEATING").data == b'[["HEATING", false]]'
    assert (
        client.get("/api/state/HEATING,UV").data
        == b'[["HEATING", false], ["UV", false]]'
    )
    assert client.get("/api/state/wontfind").data == b'[["wontfind", null]]'


def test_state_control_state_set(client):
    before = client.get("/api/state/HEATING").data
    assert before == b'[["HEATING", false]]'

    client.post("/api/state/HEATING", data=dict(state="On"))
    after = client.get("/api/state/HEATING").data
    assert after == b'[["HEATING", true]]'
    assert before != after

    client.post("/api/state/HEATING", data=dict(state="Off"))
    after2 = client.get("/api/state/HEATING").data
    assert after2 == b'[["HEATING", false]]'

    assert after2 == before


def test_error_on_sensor_set(client):
    assert (
        client.post("/api/state/SENSOR_TEMP", data=dict(state="Off")).status
        == "500 INTERNAL SERVER ERROR"
    )
    assert (
        client.post(
            "/api/state/SENSOR_TEMP,SENSOR_HUMID", data=dict(state="Off")
        ).status
        == "500 INTERNAL SERVER ERROR"
    )


def test_state_control_toggle(client):
    before = client.get("/api/state/HEATING").data
    client.post("/api/state/HEATING", data=dict(switch="1"))
    after = client.get("/api/state/HEATING").data
    client.post("/api/state/HEATING", data=dict(switch="1"))
    after2 = client.get("/api/state/HEATING").data

    assert before == b'[["HEATING", false]]'
    assert after == b'[["HEATING", true]]'
    assert after2 == b'[["HEATING", false]]'


def test_state_control_sanity_checking(client):
    assert (
        client.post("/api/state/HEATING", data=dict(switch=1, state="On")).status
        == "500 INTERNAL SERVER ERROR"
    )
    assert (
        client.post("/api/state/HEATING", data=dict(switch=0, state="Off")).status
        == "500 INTERNAL SERVER ERROR"
    )


def test_state_endpoint(client):
    assert (
        client.get("/api/state?NAME_ONLY=True").data
        == b'["HEATING", "UV", "SENSOR_TEMP", "SENSOR_HUMID"]'
    )

    assert (
        client.get("/api/state?FILTER=^SENSOR_.*&NAME_ONLY=True").data
        == b'["SENSOR_TEMP", "SENSOR_HUMID"]'
    )

    assert client.get("/api/state?FILTER=^SENSOR_.*").status == "200 OK"
