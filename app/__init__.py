import click
from os.path import join, dirname
from dotenv import load_dotenv
from app.commands.user_management import user


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


@click.group()
def cli():
    pass

cli = click.CommandCollection(sources=[user])
