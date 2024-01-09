import keyring
import click
import os
import configparser
from src.config import API_BASE_URL


def get_token():
    """Get token from keyring."""
    token = keyring.get_password('cranecloud', 'token')
    if not token:
        click.echo('Please login first.')
        exit(1)
    return token


def create_config():
    config = configparser.ConfigParser()
    config['GlobalSettings'] = {
        'base_url': API_BASE_URL
    }
    print("Please enter your CraneCloud credentials.")
    print('....................')

    home_dir = os.path.expanduser("~")
    crane_dir = os.path.join(home_dir, '.crane')

    # Create the .crane directory if it doesn't exist
    os.makedirs(crane_dir, exist_ok=True)

    config_file = os.path.join(crane_dir, 'config.ini')

    with open(config_file, 'w') as configfile:
        config.write(configfile)
