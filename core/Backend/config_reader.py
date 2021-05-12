import yaml
import pathlib, os


def read_hardware_config():
    path = os.path.join(pathlib.Path(__file__).parent.parent.absolute(), 'config.yaml')
    print(path)
    return yaml.safe_load(open(path).read())
