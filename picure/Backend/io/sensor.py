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
import random
from picure.Backend.io.implementations.sensor_shtc3 import (
    Shtc3Humidity,
    Shtc3Temperature,
)
from picure.Backend.io.prototypes.proto_sensor import SensorProto


class Sensor:
    def __new__(cls, sensor_type, name):
        if sensor_type == "SHT1_Humidity_Adafruit":
            return Shtc3Humidity(name)
        elif sensor_type == "SHT1_Temperature_Adafruit":
            return Shtc3Temperature(name)
        elif sensor_type == "Mock":
            return SensorMock(name)
        else:
            raise Exception("Sensor not yet implemented")


class SensorMock(SensorProto):
    def __init__(self, name):
        self.name = name

    def get(self, precision=4):
        return round(random.uniform(3.0, 30.50), precision)
