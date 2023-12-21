import click
import requests
from src.config import API_BASE_URL
import keyring
from tabulate import tabulate


@click.group()
def clusters_group():
    pass


@clusters_group.command('clusters', help='List all clusters.')
def get_clusters_list():
    """Get all clusters."""
    click.echo("Getting clusters list...")
    try:
        token = keyring.get_password('cranecloud', 'token')
        response = requests.get(
            f"{API_BASE_URL}/clusters", headers={'Authorization': f"Bearer {token}"})
        response.raise_for_status()
        if response.status_code == 200:
            clusters = response.json()['data']['clusters']
            click.echo(clusters)
            table_data = []
            for cluster in clusters:
                table_data.append(
                    [cluster.get('id'), cluster.get('name'),  cluster.get('description')])
            headers = ['ID', 'Name',  'Description']
            click.echo(tabulate(table_data, headers, tablefmt='simple'))
        else:
            click.echo("Failed to get clusters list.")
    except requests.RequestException as e:
        if e.response or e.response.reason:
            click.echo(f"Error: {e.response.reason}")
        else:
            click.echo(f"Failed to connect to the server: {e}")
            click.echo(
                "Please check your internet connection or try again later.")
