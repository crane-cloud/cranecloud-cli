
import os
import configparser

CONFIG_FILE = 'config'


def get_base_dir():
    home_dir = os.path.expanduser("~")
    crane_dir = os.path.join(home_dir, '.crane')
    return crane_dir


def create_config():
    default_base_url = os.getenv('API_BASE_URL', "https://api.cranecloud.io")
    write_config('base_url', default_base_url)


def read_config():
    config = configparser.ConfigParser()
    crane_dir = get_base_dir()
    config_file = os.path.join(crane_dir, CONFIG_FILE)
    config.read(config_file)
    return config


def write_config(key, value, should_update=True):
    config = configparser.ConfigParser()
    crane_dir = get_base_dir()
    config_file = os.path.join(crane_dir, CONFIG_FILE)
    os.makedirs(crane_dir, exist_ok=True)

    config.read(config_file)
    if not should_update:
        config.remove_section(key)

    if type(value) is dict:
        if not config.has_section(key):
            config.add_section(key)

        for k, v in value.items():
            config.set(str(key), str(k), str(v))
    else:
        if not config.has_section('GlobalSettings'):
            config.add_section('GlobalSettings')
        config.set('GlobalSettings', key, value)

    with open(config_file, 'w') as configfile:
        config.write(configfile)
