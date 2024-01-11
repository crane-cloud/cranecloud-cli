from src.cranecloud.utils.config import create_config, read_config

# Example usage of the config values
config_file = read_config()
try:
    API_BASE_URL = config_file['GlobalSettings']['base_url']
except KeyError:
    create_config()
    config_file = read_config()
    API_BASE_URL = config_file['GlobalSettings'].get('base_url')
try:
    CURRENT_PROJECT = config_file['current_project']
except KeyError:
    CURRENT_PROJECT = {}

try:
    CURRENT_USER = config_file['current_user']
except KeyError:
    CURRENT_USER = {}

try:
    CURRENT_CLUSTER = config_file['current_cluster']
except KeyError:
    CURRENT_CLUSTER = {}

USER_INFO_URL = {}
