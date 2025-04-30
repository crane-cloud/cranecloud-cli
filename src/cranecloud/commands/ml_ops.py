import click
import requests
import subprocess
import json

from config import MLOPS_API_BASE_URL
from cranecloud.utils import get_token
from cranecloud.core.ml_ops import MLOpsClient


mlops_client = MLOpsClient()


@click.group()
def mlops_group():
    pass


@mlops_group.group(name='mlops')
def mlops():
    """
    MLOps management commands.
    """
    pass


@mlops.command('create-experiment', help='Create an MLOps experiment.')
@click.option('--user-id', required=True, help='User ID')
@click.option('--app-alias', required=True, help='App alias')
def create_experiment(user_id, app_alias):
    """Create a new experiment ."""
    try:
        # Use the core client to do the actual work
        tracking_uri, experiment_id = mlops_client.create_experiment(
            user_id, app_alias, verbose=True)

        click.echo(f"Experiment created with ID: {experiment_id}")
        return tracking_uri, experiment_id
    except requests.exceptions.RequestException as e:
        error_data = {"error": str(e)}
        if e.response is not None:
            error_data["details"] = e.response.text
        click.echo(json.dumps(error_data))
