from src.cranecloud.commands.apps import apps_group
from src.cranecloud.commands.clusters import clusters_group
import click
from os.path import join, dirname
from dotenv import load_dotenv
from src.cranecloud.commands.user_management import user_group
from src.cranecloud.commands.projects import projects_group
from src.cranecloud.helpers import create_config


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


@click.group()
def cli():
    pass


cli = click.CommandCollection(
    sources=[user_group, projects_group, apps_group, clusters_group])


def create_initial_config():
    create_config()
