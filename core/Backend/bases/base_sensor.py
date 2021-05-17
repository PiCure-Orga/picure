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

class Sensor:

    DEV = None

    def __init__(self, sensor_type):
        if sensor_type == "SHT1_Humidity_Kernel":
            self.DEV = Sht1HumidityKd()
        elif sensor_type == "SHT1_Temperature_Kernel":
            self.DEV = Sht1TemperatureKd()
        elif sensor_type == "Mock":
            self.DEV = SensorMock()
        else:
            raise Exception("Sensor not yet implemented")

    def get_normalized_sensor_data(self, precision=2):
        return self.DEV.get_normalized_sensor_data(precision)


class Sht1HumidityKd(Sensor):
    path = "/sys/bus/i2c/devices/1-0070/hwmon/hwmon2/humidity1_input"

    def __init__(self):
        pass

    def get_normalized_sensor_data(self, precision):
        raw = open(self.path, "r").read()
        return round((100 * int(raw) / 65536), precision)


class Sht1TemperatureKd(Sensor):
    path = "/sys/bus/i2c/devices/1-0070/hwmon/hwmon2/temp1_input"

    def __init__(self):
        pass

    def get_normalized_sensor_data(self, precision):
        raw = open(self.path).read()
        return round((175 * int(raw) / 65536 - 45), precision)


class SensorMock(Sensor):
    def __init__(self):
        pass

    def get_normalized_sensor_data(self, precision):
        return round(1337.1337, precision)
