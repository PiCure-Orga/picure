[![Build](https://github.com/PiCure-Orga/picure/actions/workflows/lint_and_install.yml/badge.svg?branch=master)](https://github.com/PiCure-Orga/picure/actions/workflows/lint_and_install.yml)
[![Docker](https://github.com/PiCure-Orga/picure/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/PiCure-Orga/picure/actions/workflows/docker-publish.yml)
[![codecov](https://codecov.io/gh/PiCure-Orga/picure/branch/master/graph/badge.svg?token=BERJVA1WKV)](https://codecov.io/gh/PiCure-Orga/picure)
[![codestyle](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black#readme)

# PiCure
Dry ageing and curing with precision!

## Current state of development
PiCure has reached alpha state. This means the software basically works but I did not yet test this enought on actual hardware.

## How this all works
The whole application trys to be as modulare and portable as somehow possible. At the moment very much at the expense of a lot of usability features.
This is due to the fact that I plan to support more applications like a smoking cabinet or whatnot. This modular approach allows you to create a program
consisting of several steps varying in duration. These steps contain so called targets - a value at which we want our sensor to be during this step.

Second, you can create so called events - basically checks wether or not a sensor is above, below or equal the current steps target. If the event validates
to True a task is queued. This task Toggles, Enables or Disables a hardware actor (probably conntected to a relay). Additonaly a task can have a duration
after which the action is inverted. This comes in handy for inert sensor readings where you know the value increases significantly faster then a sensor
detects changes. 

## Setup
### Development
```python -m flask run```

### Production
```pip install .```
```gunicorn -w 2 -b 0.0.0.0:5000 "picure:create_app()"```

## License
[GNU General Public License v3.0](https://github.com/PiCure-Orga/picure/blob/master/LICENSE.txt)

