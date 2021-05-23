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


class Shtc3Humidity(SensorProto):
    def __init__(self, name):
        import board
        import adafruit_shtc3

        self.sensor = adafruit_shtc3.SHTC3(board.I2C())
        self.name = name

    def get(self, precision=2):
        return round(self.sensor.measurements[1], precision)


class Shtc3Temperature(SensorProto):
    def __init__(self, name):
        import board
        import adafruit_shtc3

        self.sensor = adafruit_shtc3.SHTC3(board.I2C())
        self.name = name

    def get(self, precision=1):
        return round(self.sensor.measurements[0], precision)
