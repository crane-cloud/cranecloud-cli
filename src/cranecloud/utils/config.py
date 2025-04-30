
import os
import configparser
from dotenv import set_key
from pathlib import Path
from os.path import join, dirname
from dotenv import load_dotenv



CONFIG_FILE = 'config'

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)



def get_base_dir():
    crane_dir = os.getenv('CRANE_CONFIG_DIR')
    if not crane_dir:
        config_dir = os.path.expanduser("~")
        crane_dir = os.path.join(config_dir, '.crane')
    return crane_dir


def create_config(dir= get_base_dir()):
    env_file_path = Path(join(dirname(__file__), '.env'))
    env_file_path.touch(mode=0o600, exist_ok=True)

    default_base_url = os.getenv('API_BASE_URL', "https://api.cranecloud.io")
    set_key(dotenv_path=env_file_path, key_to_set="CRANE_CONFIG_DIR", value_to_set=dir , export=True)
    write_config('base_url', default_base_url , crane_dir = dir)
    write_config("dotenv_path" , dotenv_path , crane_dir=env_file_path)


def create_initial_config():
    env_file_path = Path(join(dirname(__file__), '.env'))
    env_file_path.touch(mode=0o600, exist_ok=True)

    config_dir = os.path.expanduser("~")
    crane_dir = os.path.join(config_dir, '.crane')

    set_key(dotenv_path=env_file_path, key_to_set="CRANE_CONFIG_DIR", value_to_set=crane_dir , export=True)
    write_config("dotenv_path" , dotenv_path , crane_dir=crane_dir)

    default_base_url = os.getenv('API_BASE_URL', "https://api.cranecloud.io")
    write_config('base_url', default_base_url , crane_dir=crane_dir)


def read_config(crane_config = get_base_dir()):
    config = configparser.ConfigParser()
    config_file = os.path.join(crane_config, CONFIG_FILE)
    config.read(config_file)
    return config


def write_config(key, value, should_update=True , crane_dir = get_base_dir()):
    config = configparser.ConfigParser()
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
