import json
import click
import requests
from config import API_BASE_URL
import keyring
from tabulate import tabulate


@click.group()
def apps_group():
    pass


@apps_group.group(name='apps')
def apps():
    """
    App management commands.
    """
    pass


@apps.command('list', help='List apps in project')
@click.option('-p', '--project_id', type=click.UUID)
def get_apps(project_id):
    """Get apps in project."""
    click.echo("Getting apps list...")
    try:
        token = keyring.get_password('cranecloud', 'token')
        response = requests.get(
            f"{API_BASE_URL}/projects/{project_id}/apps", headers={'Authorization': f"Bearer {token}"})
        response.raise_for_status()
        if response.status_code == 200:
            apps = response.json()['data']['apps']
            click.echo(apps)
            table_data = []
            for app in apps:
                table_data.append(
                    [app['id'], app['name'], app['app_running_status'], app['url'], app['age']])
            headers = ['ID', 'Name', 'Status', 'Url', 'Age']
            click.echo(tabulate(table_data, headers, tablefmt='simple'))
        else:
            click.echo("Failed to get apps list.")
    except requests.RequestException as e:
        click.echo(f"Failed to connect to the server: {e}")
        click.echo("Please check your internet connection or try again later.")


@apps.command('info', help='Get app details.')
@click.argument('app_id', type=click.UUID)
def get_app_details(app_id):
    """Get app details."""
    click.echo("Getting app details...\n")
    try:
        token = keyring.get_password('cranecloud', 'token')
        response = requests.get(
            f"{API_BASE_URL}/apps/{app_id}", headers={'Authorization': f"Bearer {token}"})
        response.raise_for_status()
        if response.status_code == 200:
            app = response.json()['data']['apps']
            table_data = [
                ['ID', app['id']],
                ['Name', app['name']],
                ['Status', app['app_running_status']],
                ['Url', app['url']],
                ['Internal Url', app['internal_url']],
                ['Private Image', app['private_image']],
                ['Has Custom Domain', app['has_custom_domain']],
                ['Command', app['command']],
                ['Port', app['port']],
                ['Image', app['image']],
                ['Disabled', app['disabled']],
                ['Replicas', app['replicas']],
                ['Admin Disabled', app['admin_disabled']],
                ['Alias', app['alias']],
                ['Revision ID', app['revision_id']],
                ['Project ID', app['project_id']],
                ['Revision', app['revision']],
                ['Age', app['age']],
                ['Date Created', app['date_created']],
                ['Env Vars', json.dumps(app['env_vars'], indent=4)],
            ]
            click.echo(tabulate(table_data, tablefmt='plain'))
        else:
            click.echo("Failed to get app details.")
    except requests.RequestException as e:
        click.echo(f"Failed to connect to the server: {e}")
        click.echo("Please check your internet connection or try again later.")
