import click
from os.path import join, dirname
from dotenv import load_dotenv
from src.cranecloud.utils.config import create_config , write_config , get_base_dir
from src.cranecloud.commands.user_management import user_group
from src.cranecloud.commands.projects import projects_group
from src.cranecloud.commands.config_management import config_group
from src.cranecloud.commands.apps import apps_group
from src.cranecloud.commands.clusters import clusters_group
from pathlib import Path
from dotenv import set_key


@click.group()
def cli():
    pass

cli = click.CommandCollection(
    sources=[user_group, projects_group, apps_group, clusters_group, config_group])




