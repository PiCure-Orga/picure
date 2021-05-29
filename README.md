[![Python package](https://github.com/mhupfauer/picure/actions/workflows/lint_and_install.yml/badge.svg?branch=master)](https://github.com/mhupfauer/picure/actions/workflows/lint_and_install.yml)
[![Docker](https://github.com/mhupfauer/picure/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/mhupfauer/picure/actions/workflows/docker-publish.yml)
[![codecov](https://codecov.io/gh/mhupfauer/picure/branch/master/graph/badge.svg?token=BERJVA1WKV)](https://codecov.io/gh/mhupfauer/picure)
[![codestyle](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black#readme)

# PiCure
Dry ageing and curing with precision!

## Current state of development
PiCure currently reads data from SHTC3 sensor, stores it and makes it accessible in various ways.

The system can read generalized programs from the database. A program consists of one or multiple steps each containting target values that sensor should have during the
duration of a step. A program further contains events (i.e.: `if SENSOR_TEMP >/</== CURRENT_PROGRAM_STEP_TARGET['TEMP'] - 5°C`) that query a sensors value and validate it
based on a logical expression (also stored inside the database) against the target value for that sensor. If the expression validates to `True` all associated tasks of this
event will be executed. Each task can either switch on/off or toggle a `Hardware` (i.e.: `COOLING SWTICH.ON`). Further there is support for a duration in milliseconds after
which the action is inverted. These events will be validated every 10 seconds. Durations can be lower though.

## Next steps
A users should be able to create a program via the web ui

## Setup
### Development
```python -m flask run```

### Production
```gunicorn -w 2 -b 0.0.0.0:5000 "picure:create_app()"```

## License
[GNU General Public License v3.0](https://github.com/mhupfauer/picure/blob/master/LICENSE.txt)

