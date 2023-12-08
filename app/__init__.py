import click
from os.path import join, dirname
from dotenv import load_dotenv
from app.commands.user_management import get_user_info, login, logout


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


@click.group()
def cli():
    pass


cli.add_command(login)
cli.add_command(logout)
cli.add_command(get_user_info)

