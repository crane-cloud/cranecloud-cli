from cranecloud.commands.apps import apps_group
from cranecloud.commands.clusters import clusters_group
import click
from os.path import join, dirname
from dotenv import load_dotenv
from cranecloud.utils.config import create_config
from cranecloud.commands.user_management import user_group
from cranecloud.commands.projects import projects_group
from cranecloud.commands.config_management import config_group
from cranecloud.commands.ml_ops import mlops_group
from cranecloud.core.ml_ops import MLOpsClient


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


@click.group()
def cli():
    pass


cli = click.CommandCollection(
    sources=[user_group, projects_group, apps_group, clusters_group, config_group, mlops_group])

__all__ = ["MLOpsClient"]


def create_initial_config():
    create_config()
