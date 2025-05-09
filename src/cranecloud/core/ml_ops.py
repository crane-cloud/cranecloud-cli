import click
import requests
import subprocess
import logging
from config import MLOPS_API_BASE_URL
from cranecloud.utils import get_token


class MLOpsClient:
    def __init__(self):
        pass

    def create_experiment(self, token, verbose=False):
        """Create a new experiment."""
        # modify to take token as function parameter
        endpoint = f"{MLOPS_API_BASE_URL}/experiments"
        body = {
            "token": token
        }

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

        if verbose:
            print(f"Creating experiment for user with {token} ...")
        try:
            response = requests.post(endpoint, json=body, headers=headers)
            response.raise_for_status()
            result = response.json()

            tracking_uri = result.get("tracking_uri")
            experiment_id = result.get("experiment_id")

            if verbose:
                print("Experiment created successfully!")
            return tracking_uri, experiment_id
        except Exception as e:
            if verbose:
                print(f"Error: {e}")
                if e.response is not None:
                    print(e.response.text)
            raise
