import click
import requests
from config import API_BASE_URL
import keyring


@click.command('login', help='Login to CraneCloud.')
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
        if e.response and e.response.status == 401:
            click.echo("Login failed. Please check your credentials.")
        else:
            click.echo(f"Failed to connect to the server: {e}")
            click.echo(
                "Please check your internet connection or try again later.")


@click.command('logout', help='Logout user from CraneCloud.')
def logout():
    """ Logout from CraneCloud."""
    if keyring.get_password("cranecloud", "token") is None:
        click.echo("You are not logged in.")
        return
    click.echo("Logging out...")
    try:
        keyring.delete_password("cranecloud", "token")
        click.echo("Logout successful!")
    except keyring.errors.PasswordDeleteError:
        click.echo("Logout failed. Please try again later.")


@click.command('user', help='Display current user info.')
def get_user_info():
    """Get current user info."""
    click.echo("Getting user info...")
    try:
        token = keyring.get_password('cranecloud', 'token')
        user_id = keyring.get_password('cranecloud', 'user_id')
        response = requests.get(
            f"{API_BASE_URL}/users/{user_id}", headers={'Authorization': f"Bearer {token}"})
        response.raise_for_status()

        if response.status_code == 200:
            user_data = response.json()['data']['user']
            click.echo(f"Name: {user_data['name']}")
            click.echo(f"Email: {user_data['email']}")
            click.echo(f"ID: {user_data['id']}")
            click.echo(f"Projects: {user_data['projects_count']}")
        else:
            click.echo("Failed to get user info.")
    except requests.RequestException as e:
        if e.response and e.response.status == 401:
            click.echo("Failed to get user info.")
        else:
            click.echo(f"Failed to connect to the server: {e}")
            click.echo(
                "Please check your internet connection or try again later.")
