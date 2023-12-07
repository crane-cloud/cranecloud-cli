import os
import click
import requests

API_BASE_URL = os.getenv('API_BASE_URL')


@click.command('login', help='Login to CraneCloud.')
@click.option('--email', prompt=True, help='Your username')
@click.password_option(help='Your password')
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
            click.echo("Login successful!")
            # Store token or session information securely
        else:
            click.echo("Login failed. Please check your credentials.")
    except requests.RequestException as e:
        if e.response and e.response.status == 401:
            click.echo("Login failed. Please check your credentials.")
        else:
            click.echo(f"Failed to connect to the server: {e}")
            click.echo(
                "Please check your internet connection or try again later.")
