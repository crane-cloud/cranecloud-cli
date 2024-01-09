from src.cranecloud.utils.config import read_config

# Example usage of the config values
settings = read_config()['GlobalSettings']
API_BASE_URL = settings.get('base_url')

USER_INFO_URL = {}
