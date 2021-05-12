from flask import Blueprint, request, abort
from core.Backend import hardware_controller
import json

control = Blueprint("control", __name__, template_folder="templates")


@control.route("/state/<dev>", methods=["GET"])
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


@control.route("/state/<dev>", methods=["POST"])
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
