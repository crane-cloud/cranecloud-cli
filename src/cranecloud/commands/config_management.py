import click
from tabulate import SEPARATING_LINE, tabulate
from src.cranecloud.commands.projects import set_use_project
from src.config import CURRENT_CLUSTER, CURRENT_PROJECT, CURRENT_USER
from src.cranecloud.utils.config import read_config


@click.group()
def config_group():
    pass


@config_group.group(name='config')
def config():
    """
    Config management commands.
    """
    pass


@config.command('get-config', help='CraneCloud configuration.')
def get_config():
    """Get CraneCloud configuration."""
    click.echo('Getting CraneCloud configuration...')
    config_file = read_config()
    try:
        global_settings = config_file['GlobalSettings']
    except KeyError:
        global_settings = {}

    current_project = f"id:\t{CURRENT_PROJECT.get('id')} \nname:\t{CURRENT_PROJECT.get('name')}" if CURRENT_PROJECT else None
    current_cluster = f"id:\t{CURRENT_CLUSTER.get('id')} \nname:\t{CURRENT_CLUSTER.get('name')}" if CURRENT_CLUSTER else None
    current_user = f"name:\t{CURRENT_USER.get('name')} \nemail:\t{CURRENT_USER.get('email')}" if CURRENT_USER else None

    config_data = {
        'base_url': global_settings.get('base_url'),
        'current_project': current_project,
        'current_user': current_user,
        'current_cluster': current_cluster,
    }
    table_data = []
    for key, value in config_data.items():
        table_data.append([key, value])
    headers = ['Key', 'Value']
    click.echo(tabulate(table_data, headers, tablefmt='simple'))
