import click
from tabulate import tabulate
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

    try:
        user_settings = config_file['current_user']
    except KeyError:
        user_settings = {}

    config_data = {
        'base_url': global_settings.get('base_url'),
        'current_project': global_settings.get('current_project'),
        'current_cluster': global_settings.get('current_cluster'),
        'current_user': user_settings.get('email'),
    }
    table_data = []
    for key, value in config_data.items():
        table_data.append([key, value])
    headers = ['Key', 'Value']
    click.echo(tabulate(table_data, headers, tablefmt='simple'))
