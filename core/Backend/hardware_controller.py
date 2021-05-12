from core.Backend import config_reader
from core.Backend.bases.base_hardware import Hardware
from core.Backend.bases.base_sensor import Sensor

installed_hardware = {}


def setup_hardware():
    hw_config = config_reader.read_hardware_config()
    for hardware in hw_config.items():
        global installed_hardware
        if hardware[1].get("TYPE") == "Hardware":
            installed_hardware[hardware[0]] = Hardware(hardware[1].get("GPIO"), hardware[1].get("HARDWARE_TYPE"))
        elif hardware[1].get("TYPE") == "Sensor":
            installed_hardware[hardware[0]] = Sensor(hardware[1].get("SENSOR_TYPE"))
        else:
            raise Exception("CONFIG Property '" + str(hardware[1].get("TYPE")) + "' not implemented")


def get_hardware_states():
    if len(installed_hardware) == 0:
        setup_hardware()

    to_return = {}

    for hardware in installed_hardware.items():
        if isinstance(hardware[1], Sensor):
            to_return[hardware[0]] = hardware[1].get_normalized_sensor_data()
        if isinstance(hardware[1], Hardware):
            to_return[hardware[0]] = hardware[1].get_state()

    return to_return


def get_all_sensor_data():
    if len(installed_hardware) == 0:
        setup_hardware()

    to_return = {}

    for hardware in installed_hardware.items():
        if isinstance(hardware[1], Sensor):
            to_return[hardware[0]] = hardware[1].get_normalized_sensor_data()

    return to_return
