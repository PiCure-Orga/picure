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

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import relativedelta
import datetime
import json

data = json.loads(input('Paste output from /data/<sensor>/<minute>:'))
seconds = [datetime.datetime.fromtimestamp(s[0]) for s in data]
values = [s[2] for s in data]

delta = relativedelta.relativedelta(max(seconds), min(seconds))
locator = None

if (delta.hours > 10):
    locator = mdates.HourLocator(interval=2)
elif (5 < delta.hours <= 10):
    locator = mdates.HourLocator(interval=1)
elif (delta.hours <= 5):
    locator = mdates.MinuteLocator(interval=30)
elif (delta.hours <= 0 and delta.minutes > 30):
    locator = mdates.MinuteLocator(interval=3)
elif (delta.hours <= 0 and delta.minutes < 30):
    locator = mdates.MinuteLocator(interval=1)

plt.plot(seconds, values)
plt.gca().xaxis.set_major_locator(locator=locator)
plt.show()
