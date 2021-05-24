[![Python package](https://github.com/mhupfauer/picure/actions/workflows/lint_and_install.yml/badge.svg?branch=master)](https://github.com/mhupfauer/picure/actions/workflows/lint_and_install.yml)
[![Publish Python Package](https://github.com/mhupfauer/picure/actions/workflows/publish-wheel.yml/badge.svg)](https://github.com/mhupfauer/picure/actions/workflows/publish-wheel.yml)
[![Docker](https://github.com/mhupfauer/picure/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/mhupfauer/picure/actions/workflows/docker-publish.yml)
[![codecov](https://codecov.io/gh/mhupfauer/picure/branch/master/graph/badge.svg?token=BERJVA1WKV)](https://codecov.io/gh/mhupfauer/picure)
[![codestyle](https://img.shields.io/badge/code%20style-black-black)

# PiCure
Dry ageing and curing with precision!

## Current state of development
PiCure currently reads data from SHTC3 sensor, stores it and makes it accessible via varios ways.

## Next steps
The next step will be the implementation of the cure program logic, that enables an enduser to define several recepies for curing with steps defining values that should be reached. The user then sould be enabled to define events like `if SENSOR_TEMP is below CURE_PROGRAM_TARGET['TEMP'] - 5°C` that execut an action_set. Consisting of `name` and `actions` where each action referencing the `actor` (i.e. Hardware) and a `ActionTask` that defines the translation of the the `actors` state. (i.e. ActionState.SWITCH_OFF, ActionState.SWITCH_OF, ActionState.TOGGLE). A recurring programm will evaluate all events and execute their action_sets actions if their condition matches.

## Setup
### Development
```python -m flask run```

### Production
```gunicorn -w 2 -b 0.0.0.0:5000 "picure:create_app()"```

## License
[GNU General Public License v3.0](https://github.com/mhupfauer/picure/blob/master/LICENSE.txt)

