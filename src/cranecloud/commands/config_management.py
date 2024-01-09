import click
import requests
from src.config import API_BASE_URL
import keyring
from src.cranecloud.helpers import get_token


@click.group()
def config_group():
    pass


@config_group.group(name='auth')
def config():
    """
    Config management commands.
    """
    pass


@config.command('login', help='Login to CraneCloud.')
@click.option('-e', '--email', prompt=True, help='Your username', type=str)
@click.password_option('-p', '--password', help='Your password')
def login(email, password):
    """Login to CraneCloud."""
    click.echo("Logging in...")
    login_data = {
        'email': email,
        'password': password
    }
    try:
        response = requests.post(
            f"{API_BASE_URL}/users/login", json=login_data)
        response.raise_for_status()
        if response.status_code == 200:
            user_body = response.json()['data']
            keyring.set_password("cranecloud", "token",
                                 user_body['access_token'])
            keyring.set_password("cranecloud", "user_id", user_body['id'])
            click.echo("Login successful!")
        else:
            click.echo("Login failed. Please check your credentials.")
    except requests.RequestException as e:
        if e.response or e.response.status_code == 401:
            click.echo("Login failed. Please check your credentials.")
        elif e.response and e.response.reason:
            click.echo(f"Failed to login: {e.response.reason}")
        else:
            click.echo(f"Failed to connect to the server: {e}")
            click.echo(
                "Please check your internet connection or try again later.")

