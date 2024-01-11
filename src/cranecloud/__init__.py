from src.cranecloud.commands.apps import apps_group
from src.cranecloud.commands.clusters import clusters_group
import click
from os.path import join, dirname
from dotenv import load_dotenv
from src.cranecloud.utils.config import create_config
from src.cranecloud.commands.user_management import user_group
from src.cranecloud.commands.projects import projects_group
from src.cranecloud.commands.config_management import config_group


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


@click.group()
def cli():
    pass


cli = click.CommandCollection(
    sources=[user_group, projects_group, apps_group, clusters_group, config_group])


def create_initial_config():
    create_config()
