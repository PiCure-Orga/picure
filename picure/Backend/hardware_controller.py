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
from picure.Backend.io.prototypes.proto_sensor import SensorProto

from picure.Backend import config_reader
from picure.Backend.io.hardware import Hardware
from picure.Backend.io.sensor import Sensor

installed_hardware = {}


def setup_hardware():
    hw_config = config_reader.read_hardware_config()
    for hardware in hw_config.items():
        global installed_hardware

        if hardware[1].get("TYPE") == "Hardware":
            installed_hardware[hardware[0]] = Hardware(
                pin=hardware[1].get("GPIO"),
                hardware=hardware[1].get("HARDWARE_TYPE"),
                name=hardware[0],
            )
        elif hardware[1].get("TYPE") == "Sensor":
            installed_hardware[hardware[0]] = Sensor(
                sensor_type=hardware[1].get("SENSOR_TYPE"), name=hardware[0]
            )
        else:
            raise Exception(
                "CONFIG Property '" + str(hardware[1].get("TYPE")) + "' not implemented"
            )


def get_hardware_states():
    if len(installed_hardware) == 0:
        setup_hardware()

    return {hardware[0]: hardware[1].get() for hardware in installed_hardware.items()}


def get_all_sensor_data():
    if len(installed_hardware) == 0:
        setup_hardware()

    return {
        hardware[0]: hardware[1].get()
        for hardware in installed_hardware.items()
        if issubclass(type(hardware[1]), SensorProto)
    }


def get_hardware(hardware):
    if len(installed_hardware) == 0:
        setup_hardware()
    return installed_hardware[hardware]
