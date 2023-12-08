from app.commands.apps import apps_group
from app.commands.clusters import clusters_group
import click
from os.path import join, dirname
from dotenv import load_dotenv
from app.commands.user_management import user_group
from app.commands.projects import projects_group


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


@click.group()
def cli():
    pass


cli = click.CommandCollection(
    sources=[user_group, projects_group, apps_group, clusters_group])
