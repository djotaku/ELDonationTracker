import logging

__version__ = "7.4.4"

base_api_url: str = "https://www.extra-life.org/api"
api_version_suffix: str = "?version=1.2"
file_logging = logging.FileHandler('eldonationtracker_log.txt', 'w')
file_logging.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_logging.setFormatter(formatter)
