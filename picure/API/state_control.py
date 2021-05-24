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
import re
from flask import Blueprint, request, abort
from picure.Backend import hardware_controller
import json

control = Blueprint("control", __name__, template_folder="templates")


@control.route("/state", methods=["GET"])
def state():
    filter_param = request.args.get("FILTER")
    nameonly_param = request.args.get("NAME_ONLY")
    data = None
    hw_states = hardware_controller.get_hardware_states()

    if filter_param is None:
        data = hw_states
    else:
        data = {
            hw[0]: hw[1] for hw in hw_states.items() if re.match(filter_param, hw[0])
        }

    if str(nameonly_param).lower() == "true":
        data = [d[0] for d in data.items()]

    return json.dumps(data)


@control.route("/state/<string:dev>", methods=["GET"])
def get(dev):
    requested = dev.split(",")
    installed_hardware = hardware_controller.get_hardware_states()
    return json.dumps([[req, installed_hardware.get(req)] for req in requested])


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
        for device in requested:
            if str(form_data["state"]).lower() in ("true", "yes", "on", "1"):
                hardware_controller.get_hardware(dev).on()
            else:
                hardware_controller.get_hardware(dev).off()

    # Handling for switch, no need for sanity checking - we'll accept any value
    if "switch" in form_data:
        for device in requested:
            hardware_controller.get_hardware(dev).toggle()

    return get(dev)
