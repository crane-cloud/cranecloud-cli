from src.cranecloud.commands.apps import apps , revisions
from src.cranecloud.commands.clusters import clusters
import click
from os.path import join, dirname
from dotenv import load_dotenv
from src.cranecloud.utils.config import create_config
from src.cranecloud.commands.user_management import user
from src.cranecloud.commands.projects import projects
from src.cranecloud.commands.config_management import config



dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


@click.group()
def cli():
    pass

#Users Section
cli.add_command(user)


#Projects section
cli.add_command(projects)


# Apps section
apps.add_command(revisions)
cli.add_command(apps)

# Clusters section
cli.add_command(clusters)


# Config section
cli.add_command(config)






def create_initial_config():
    create_config()

if __name__ == '__main__':
    cli()
