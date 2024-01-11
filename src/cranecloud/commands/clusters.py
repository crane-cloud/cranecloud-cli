import click
import requests
from src.cranecloud.utils.config import write_config
from src.config import API_BASE_URL, CURRENT_CLUSTER
from tabulate import tabulate

from src.cranecloud.utils import get_token


@click.group()
def clusters_group():
    pass


@clusters_group.group(name='clusters')
def clusters():
    '''
    App management commands.
    '''
    pass


@clusters.command('list', help='List all clusters.')
def get_clusters_list():
    """Get all clusters."""
    click.echo("Getting clusters list...")
    try:
        token = get_token()
        response = requests.get(
            f"{API_BASE_URL}/clusters", headers={'Authorization': f"Bearer {token}"})
        response.raise_for_status()
        if response.status_code == 200:
            clusters = response.json()['data']['clusters']
            table_data = []
            for cluster in clusters:
                cluster_name = cluster.get('name')+' *' if cluster.get(
                    'id') == CURRENT_CLUSTER.get('id') else cluster.get('name')
                table_data.append(
                    [cluster.get('id'), cluster_name,  cluster.get('description')])
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


@clusters.command('use-cluster', help='Set current cluster to use')
@click.argument('cluster_id', type=click.UUID)
def set_use_cluster(cluster_id):
    """set current cluster to use"""
    click.echo("Setting current cluster...")
    try:
        token = get_token()
        response = requests.get(
            f"{API_BASE_URL}/clusters", headers={'Authorization': f"Bearer {token}"})
        response.raise_for_status()
        if response.status_code == 200:
            clusters = response.json()['data']['clusters']
            cluster = next(
                (cluster for cluster in clusters if cluster['id'] == str(cluster_id)), {})
            if not cluster:
                click.echo('Error: Cluster does not exist')
                return
            write_config('current_cluster', {
                'id': cluster.get('id'),
                'name': cluster.get('name')
            })
            click.echo(f"Cluster id {cluster_id} set successfully.")
        else:
            click.echo("Failed to get cluster details.")
    except requests.RequestException as e:
        if e.response or e.response.status_code == 404:
            click.echo('Cluster does not exist')
        elif e.response or e.response.reason:
            click.echo(f"Error: {e.response.reason}")
        else:
            click.echo(f"Failed to connect to the server: {e}")
            click.echo(
                "Please check your internet connection or try again later.")
