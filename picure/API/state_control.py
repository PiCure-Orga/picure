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

from flask import Blueprint, request, abort
from picure.Backend import hardware_controller
import json

control = Blueprint("control", __name__, template_folder="templates")


@control.route("/state/<string:dev>", methods=["GET"])
def get(dev):
    installed_hardware = hardware_controller.get_hardware_states()
    requested = dev.split(",")
    result = []
    for req in requested:
        if req in installed_hardware:
            result.append([req, installed_hardware.get(req)])
        else:
            result.append([req, "Not found"])

    return json.dumps(result)


@control.route("/state/<string:dev>", methods=["POST"])
def post(dev):
    installed_hardware = hardware_controller.get_hardware_states()
    requested = dev.split(",")
    form_data = request.form.to_dict()

    for d in requested:
        if not isinstance(installed_hardware.get(d), bool):
            abort(500, "Cant set sensor data")

    # Sanity check whether or not both fields are present
    if "switch" in form_data and "state" in form_data:
        abort(500, "Switch and State fields may not be present simultaneously!")

    # State handling
    if "state" in form_data:
        # Why not check for more than true... May come in handy sometime.
        state = str(form_data["state"]).lower() in ("true", "yes", "on", "1")
        for device in requested:
            installed_hardware[device] = state

    # Handling for switch, no need for sanity checking - we'll accept any value
    if "switch" in form_data:
        for device in requested:
            installed_hardware[device] = not installed_hardware[device]

    return get(dev)
