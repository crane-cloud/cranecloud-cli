import click
import requests
import subprocess
import logging
from config import MLOPS_API_BASE_URL
from cranecloud.utils import get_token

class MLOpsClient:
    def __init__(self):
        pass

    def create_experiment(self, user_id, app_alias, verbose=False):
        """Create a new experiment."""
        token = get_token()
        endpoint = f"{MLOPS_API_BASE_URL}/experiments"
        params = {
            "user_id": user_id,
            "app_alias": app_alias
        }

        headers = {
            "accept": "application/json"
        }

        if verbose: print(f"Creating experiment for user '{user_id}' on app '{app_alias}'...")
        try:
            response = requests.post(endpoint, params=params, headers=headers)
            response.raise_for_status()
            result = response.json()

            tracking_uri = result.get("tracking_uri")
            experiment_id = result.get("experiment_id")
            
            if verbose: print("✅ Experiment created successfully!")
            return tracking_uri, experiment_id
        except requests.exceptions.RequestException as e:
            if verbose:
                print(f"Error: {e}")
                if e.response is not None:
                    print(e.response.text)
            raise


