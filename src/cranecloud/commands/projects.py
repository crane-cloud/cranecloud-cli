import click
import requests
from tabulate import tabulate
from src.config import (API_BASE_URL, CURRENT_PROJECT,
                        CURRENT_CLUSTER, CURRENT_USER)
from src.cranecloud.utils.config import write_config

from src.cranecloud.utils import get_token


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
        token = get_token()
        response = requests.get(
            f"{API_BASE_URL}/projects", headers={'Authorization': f"Bearer {token}"})
        response.raise_for_status()

        if response.status_code == 200:
            projects = response.json()['data']['projects']
            table_data = []
            for project in projects:
                project_name = project.get('name')+' *' if project.get(
                    'id') == CURRENT_PROJECT.get('id') else project.get('name')
                table_data.append(
                    [project.get('id'),
                     project_name,
                     project.get('apps_count'),
                     project.get('disabled'),
                     project.get('age')])
            headers = ['ID', 'Name', 'Apps Count', 'Disabled', 'Age']
            click.echo(tabulate(table_data, headers, tablefmt='simple'))
        else:
            click.echo("Failed to get projects list.")
    except requests.RequestException as e:
        if e.response not in [None, '']:
            try:
                click.echo(
                    click.style(f'Error\n', fg='red') +
                    e.response.json().get('message'))
            except:
                click.echo(
                    click.style(f'Error\n', fg='red') +
                    e.response.text)
        else:
            click.echo(f"Failed to connect to the server: {e}")
            click.echo(
                "Please check your internet connection or try again later.")


@projects.command('create', help='Create a new project.')
@click.option('-n', '--name', type=str, help='Project name', required=True)
@click.option('-d', '--description', type=str, help='Project description', required=True)
@click.option('-t', '--project_type', type=str, help='Project type', required=True)
@click.option('-o', '--organisation', type=str, help='Project organisation', required=True)
@click.option('-c', '--cluster_id', type=click.UUID, help='Cluster ID')
def create_project(name, description, project_type, organisation, cluster_id):
    """Create a new project."""
    click.echo("Creating project...")
    try:
        try:
            cluster_id = cluster_id or CURRENT_CLUSTER['id']
        except KeyError:
            click.echo(
                'Error: Please specify a cluster_id or \n\tset a current cluster using cranecloud clusters use-cluster')
            return
        token = get_token()
        response = requests.post(
            f"{API_BASE_URL}/projects",
            headers={'Authorization': f"Bearer {token}"},
            json={
                'name': name,
                'description': description,
                'project_type': project_type,
                'organisation': organisation,
                'cluster_id': cluster_id,
                'owner_id': CURRENT_USER['id']
            }
        )
        response.raise_for_status()
        if response.status_code == 201:
            click.echo("Project created successfully.")
        else:
            click.echo("Failed to create project.")
    except requests.RequestException as e:
        if e.response or e.response.reason:
            click.echo(click.style(f'Error: {e.response.text}\n', fg='red'))
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
        token = get_token()
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
        token = get_token()
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


@projects.command('use-project', help='Set current project to use')
@click.argument('project_id', type=click.UUID)
def set_use_project(project_id):
    """set current project to use"""
    click.echo("Setting current project...")
    try:
        token = get_token()
        response = requests.get(
            f"{API_BASE_URL}/projects/{project_id}", headers={'Authorization': f"Bearer {token}"})
        response.raise_for_status()
        if response.status_code == 200:
            project = response.json()['data']['project']
            write_config('current_project', {
                'id': project.get('id'),
                'name': project.get('name'),
                'apps_count': project.get('apps_count')})
            click.echo(f"Project id {project_id} set successfully.")
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
