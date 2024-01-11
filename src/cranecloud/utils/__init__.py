import keyring
import click


def get_token():
    """Get token from keyring."""
    token = keyring.get_password('cranecloud', 'token')
    if not token:
        click.echo('Please login first.')
        exit(1)
    return token


