import click
import requests
from src.config import API_BASE_URL
import keyring
from tabulate import tabulate


@click.group()
def projects_group():
    pass


@projects_group.group(name='projects')
def projects():
    """
    Project management commands.
    """
    pass


@projects.command('list', help='List all projects.')
def get_projects_list():
    """Get all projects."""
    click.echo("Getting projects list...")
    try:
        token = keyring.get_password('cranecloud', 'token')
        response = requests.get(
            f"{API_BASE_URL}/projects", headers={'Authorization': f"Bearer {token}"})
        response.raise_for_status()
        if response.status_code == 200:
            projects = response.json()['data']['projects']
            table_data = []
            for project in projects:
                table_data.append(
                    [project.get('id'), project.get('name'), project.get('apps_count'), project.get('disabled'), project.get('age')])
            headers = ['ID', 'Name', 'Apps Count', 'Disabled', 'Age']
            click.echo(tabulate(table_data, headers, tablefmt='simple'))
        else:
            click.echo("Failed to get projects list.")
    except requests.RequestException as e:
        if e.response not in [None, '']:
            click.echo(
                click.style(f'Error\n', fg='red') +
                e.response.json().get('message'))
        else:
            click.echo(f"Failed to connect to the server: {e}")
            click.echo(
                "Please check your internet connection or try again later.")


@projects.command('info', help='Get project details.')
@click.argument('project_id', type=click.UUID)
def get_project_details(project_id):
    """Get project details."""
    click.echo("Getting project details...")
    try:
        token = keyring.get_password('cranecloud', 'token')
        response = requests.get(
            f"{API_BASE_URL}/projects/{project_id}", headers={'Authorization': f"Bearer {token}"})
        response.raise_for_status()
        if response.status_code == 200:
            project = response.json()['data']['project']
            table_data = [
                ['ID', project.get('id')],
                ['Name', project.get('name')],
                ['Project Type', project.get('project_type')],
                ['Apps Count', project.get('apps_count')],
                ['Cluster ID', project.get('cluster_id')],
                ['Organisation', project.get('organisation')],
                ['Description', project.get('description')],
                ['Disabled', project.get('disabled')],
                ['Age', project.get('age')],
                ['Created at', project.get('date_created')]
            ]
            click.echo(tabulate(table_data,  tablefmt='plain'))

        else:
            click.echo("Failed to get project details.")
    except requests.RequestException as e:
        if e.response or e.response.status_code == 404:
            click.echo('Project does not exist')
        elif e.response or e.response.reason:
            click.echo(f"Error: {e.response.reason}")
        else:
            click.echo(f"Failed to connect to the server: {e}")
            click.echo(
                "Please check your internet connection or try again later.")


@projects.command('delete', help='Delete Project')
@click.argument('project_id', type=click.UUID)
def delete_project(project_id):
    """Delete project."""
    click.echo("Deleting project...")
    try:
        token = keyring.get_password('cranecloud', 'token')
        response = requests.delete(
            f"{API_BASE_URL}/projects/{project_id}", headers={'Authorization': f"Bearer {token}"})
        response.raise_for_status()
        if response.status_code == 200:
            click.echo("Project deleted successfully.")
        else:
            click.echo("Failed to delete project.")
    except requests.RequestException as e:
        if e.response or e.response.status_code == 404:
            click.echo('Project does not exist')
        elif e.response or e.response.reason:
            click.echo(f"Failed to delete project: {e.response.reason}")
        else:
            click.echo(f"Failed to connect to the server: {e}")
            click.echo(
                "Please check your internet connection or try again later.")
