from setuptools import setup, find_packages

setup(
    name="picure",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask~=1.1.2",
        "gpiozero~=1.6.2",
        "PyYAML~=5.4.1",
        "APScheduler~=3.7.0",
        "setuptools~=56.0.0",
        "sqlalchemy~=1.4.15",
        "Flask-APScheduler~=1.12.2",
        "adafruit-blinka~=6.9.1",
        "adafruit-circuitpython-shtc3~=1.1.1",
    ],
    zip_safe=False,
    url="https://github.com/mhupfauer/picure",
    license="GNU General Public License v3.0",
    author="Markus Hupfauer",
    author_email="markus@hupfauer.one",
    description="picure - meat curing and dry ageing",
)
