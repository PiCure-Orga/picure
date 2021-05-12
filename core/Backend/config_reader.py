import yaml
import pathlib, os


def read_hardware_config():
    path = os.path.join(pathlib.Path().absolute(), 'core', 'config.yaml')
    return yaml.safe_load(open(path).read())
