import json
import click
import requests
from src.config import API_BASE_URL
from tabulate import tabulate
from src.config import CURRENT_PROJECT
from src.cranecloud.utils import get_token


@click.group()
def apps_group():
    pass


@apps_group.group(name='apps')
def apps():
    '''
    App management commands.
    '''
    pass


@apps.command('list', help='List apps in project')
@click.option('-p', '--project_id', type=click.UUID, help='Project ID')
def get_apps(project_id):
    '''Get apps in project.'''
    click.echo('Getting apps list...')
    try:
        project_id = project_id or CURRENT_PROJECT['id']
    except KeyError:
        click.echo(
            'Error: Please specify a project_id or \n\tset a current project using cranecloud projects use-project')
        return
    try:
        token = get_token()
        response = requests.get(
            f'{API_BASE_URL}/projects/{project_id}/apps', headers={'Authorization': f'Bearer {token}'})
        response.raise_for_status()
        if response.status_code == 200:
            apps = response.json()['data']['apps']
            table_data = []
            for app in apps:
                table_data.append(
                    [app.get('id'), app.get('name'), app.get('app_running_status'), app.get('url'), app.get('age')])
            headers = ['ID', 'Name', 'Status', 'Url', 'Age']
            click.echo(tabulate(table_data, headers, tablefmt='simple'))
        else:
            click.echo('Failed to get apps list.')
    except requests.RequestException as e:
        if e.response or e.response.reason:
            click.echo(f'Error: {e.response.reason}')
        else:
            click.echo(f'Failed to connect to the server: {e}')
            click.echo(
                'Please check your internet connection or try again later.')


@apps.command('info', help='Get app details.')
@click.argument('app_id', type=click.UUID)
def get_app_details(app_id):
    '''Get app details.'''
    click.echo('Getting app details...\n')
    try:
        token = get_token()
        response = requests.get(
            f'{API_BASE_URL}/apps/{app_id}', headers={'Authorization': f'Bearer {token}'})
        response.raise_for_status()
        if response.status_code == 200:
            app = response.json()['data']['apps']
            table_data = [
                ['ID', app.get('id')],
                ['Name', app.get('name')],
                ['Status', app.get('app_running_status')],
                ['Url', app.get('url')],
                ['Internal Url', app.get('internal_url')],
                ['Private Image', app.get('private_image')],
                ['Has Custom Domain', app.get('has_custom_domain')],
                ['Command', app.get('command')],
                ['Port', app.get('port')],
                ['Image', app.get('image')],
                ['Disabled', app.get('disabled')],
                ['Replicas', app.get('replicas')],
                ['Admin Disabled', app.get('admin_disabled')],
                ['Alias', app.get('alias')],
                ['Revision ID', app.get('revision_id')],
                ['Project ID', app.get('project_id')],
                ['Revision', app.get('revision')],
                ['Age', app.get('age')],
                ['Date Created', app.get('date_created')],
                ['Env Vars', json.dumps(app.get('env_vars'), indent=4)],
            ]
            click.echo(tabulate(table_data, tablefmt='plain'))
        else:
            click.echo('Failed to get app details.')
    except requests.RequestException as e:
        if e.response or e.response.status_code == 404:
            click.echo('App does not exist')
        elif e.response or e.response.reason:
            click.echo(f'Error: {e.response.reason}')
        else:
            click.echo(f'Failed to connect to the server: {e}')
            click.echo(
                'Please check your internet connection or try again later.')


@apps.command('delete', help='Delete App')
@click.argument('app_id', type=click.UUID)
def delete_app(app_id):
    '''Delete app.'''
    click.echo('Deleting app...')
    try:
        token = get_token()
        response = requests.delete(
            f'{API_BASE_URL}/apps/{app_id}', headers={'Authorization': f'Bearer {token}'})
        response.raise_for_status()
        if response.status_code == 200:
            click.echo('App deleted successfully.')
        else:
            click.echo('Failed to delete app.')
    except requests.RequestException as e:
        if e.response or e.response.status_code == 404:
            click.echo('App does not exist')
        elif e.response or e.response.reason:
            click.echo(f'Failed to delete app: {e.response.reason}')
        else:
            click.echo(f'Failed to connect to the server: {e}')
            click.echo(
                'Please check your internet connection or try again later.')


@apps.command('deploy', help='Deploy an application')
@click.option('-n', '--name', type=str, required=True, help='App name')
@click.option('-i', '--image', type=str, required=True, help='App image')
@click.option('-c', '--command', type=str, default='', help='App command')
@click.option('-r', '--replicas', type=int, default=1, help='App replicas, default is 1')
@click.option('-o', '--port', type=int, default=80, help='App port, default is 80')
@click.option('-e', '--env', multiple=True, help='Environment variables in key=value format')
@click.option('-p', '--project_id', type=click.UUID, help='Project ID')
def deploy_app(project_id, name, image, command, replicas, port, env):
    '''Deploy an application.'''
    click.echo('Deploying app...')

    try:
        project_id = project_id or CURRENT_PROJECT['id']
    except KeyError:
        click.echo(
            'Error: Please specify a project_id or \n\tset a current project using cranecloud projects use-project')
        return

    try:
        token = get_token()
        data = {
            'name': name,
            'command': command,
            'image': image,
            'replicas': replicas,
            'port': port,
            # Convert list of env variables to a dictionary
            'env_vars': dict(v.split('=') for v in env)

        }

        response = requests.post(
            f'{API_BASE_URL}/projects/{project_id}/apps',
            headers={'Authorization': f'Bearer {token}'},
            json=data
        )
        response.raise_for_status()
        click.echo('App deployed successfully.')
    except requests.RequestException as e:
        if e.response not in [None, '']:
            click.echo(
                click.style(f'Failed to deploy app\n', fg='red') +
                e.response.json().get('message'))
        else:
            click.echo(f'Failed to connect to the server: {e}')
            click.echo(
                'Please check your internet connection or try again later.')


@apps.command('update', help='Update an application')
@click.argument('app_id', type=click.UUID)
@click.option('-n', '--name', type=str, help='App name')
@click.option('-i', '--image', type=str, help='App image')
@click.option('-c', '--command', type=str,  help='App command')
@click.option('-r', '--replicas', type=int,  help='App replicas')
@click.option('-o', '--port', type=int,  help='App port')
@click.option('-e', '--env', multiple=True, help='Environment variables in key=value format. eg -e KEY=value, -e KEY2=value2')
def update_app(app_id, name, image, command, replicas, port, env):
    '''Update an application.'''
    click.echo('Updating application...')
    try:
        token = get_token()
        data = {}
        if name:
            data['name'] = name
        if command:
            data['command'] = command
        if image:
            data['image'] = image
        if replicas:
            data['replicas'] = replicas
        if port:
            data['port'] = port
        if env:
            data['env_vars'] = dict(v.split('=') for v in env)

        if not data:
            click.echo('Opps, No update data provided.')
            return
        response = requests.patch(
            f'{API_BASE_URL}/apps/{app_id}',
            headers={'Authorization': f'Bearer {token}'},
            json=data
        )
        response.raise_for_status()
        click.echo('App updated successfully.')
    except requests.RequestException as e:
        if e.response not in [None, '']:
            click.echo(
                click.style(f'Failed to update app\n', fg='red') +
                e.response.json().get('message'))
        else:
            click.echo(f'Failed to connect to the server: {e}')
            click.echo(
                'Please check your internet connection or try again later.')
