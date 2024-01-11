import click
import requests
from src.config import API_BASE_URL
import keyring
from tabulate import tabulate
from src.cranecloud.utils import get_token
from src.cranecloud.utils.config import write_config


@click.group()
def user_group():
    pass


@user_group.group(name='auth')
def user():
    """
    User management commands.
    """
    pass


@user.command('login', help='Login to CraneCloud.')
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
            write_config('current_user', {
                'id': user_body['id'],
                'name': user_body['name'],
                'email': user_body['email']})
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


@user.command('logout', help='Logout user from CraneCloud.')
def logout():
    """ Logout from CraneCloud."""
    write_config('current_user', "Null", should_update=False)
    if keyring.get_password("cranecloud", "token") is None:
        click.echo("You are not logged in.")
        return
    click.echo("Logging out...")
    try:
        keyring.delete_password("cranecloud", "token")
        click.echo("Logout successful!")
    except keyring.errors.PasswordDeleteError:
        click.echo("Logout failed. Please try again later.")


@user.command('user', help='Display current user info.')
def get_user_info():
    """Get current user info."""
    click.echo("Getting user info...\n")
    try:
        token = get_token()
        user_id = keyring.get_password('cranecloud', 'user_id')
        response = requests.get(
            f"{API_BASE_URL}/users/{user_id}", headers={'Authorization': f"Bearer {token}"})
        response.raise_for_status()

        if response.status_code == 200:
            user_data = response.json()['data']['user']
            table_data = [
                ['ID', user_data.get('id')],
                ['Name', user_data.get('name')],
                ['Email', user_data.get('email')],
                ['Organisation', user_data.get('organisation')],
                ['Verified', user_data.get('verified')],
                ['Projects Count', user_data.get('projects_count')],
                ['Apps Count', user_data.get('apps_count')],
                ['Database Count', user_data.get('database_count')],
                ['Age', user_data.get('age')],
                ['Created At', user_data.get('date_created')]
            ]
            click.echo(tabulate(table_data, tablefmt='simple'))
        else:
            click.echo("Failed to get user info.")
    except requests.RequestException as e:
        if e.response or e.response.status_code == 401:
            click.echo("Failed to get user info.")
        elif e.response or e.response.reason:
            click.echo(f"Error: {e.response.reason}")
        else:
            click.echo(f"Failed to connect to the server: {e}")
            click.echo(
                "Please check your internet connection or try again later.")
