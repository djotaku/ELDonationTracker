"""A utility to determine if there is a newer version available."""
import json
import logging

import requests
import semver  # type: ignore

from eldonationtracker import __version__ as pkg_current_version
from eldonationtracker import file_logging

# logging
update_log = logging.getLogger("update checker")
update_log.addHandler(file_logging)


def get_pypi_version(url: str) -> str:
    """Use PyPi JSON API to get the latest version.

    :return: A string with the version number.
    """
    try:
        payload = requests.get(url)
    except requests.Timeout:
        update_log.error("Timed out trying to get to the PyPi URL")
        return "Error"
    try:
        this_program_json = payload.json()
        if this_program_json.get('message') == "Not Found":
            return "Error"
    except json.JSONDecodeError:
        update_log.error("Could not get JSON. Perhaps, the URL did not return JSON.")
        return "Error"
    return this_program_json.get("info").get("version")


def update_available(pypi_version: str, current_version: str) -> bool:
    """Use semver module to calculate whether there is a newer version on PyPi.

    :return: True if the PyPi version is higher than the version being run.\
    Returns false if the version being compared to PyPi is equal or greater\
    than the PyPi version."""
    if semver.compare(pypi_version, current_version) == 1:
        update_log.info(f"There is an update available. PyPi version: {pypi_version}")
        return True
    else:
        update_log.info("You have the latest version.")
        return False


def main() -> bool:
    """Get the latest version on PyPi and compare to current version.

    Made the decision to return false if the URL couldn't be reached rather than make the user look for an update\
    that might not be there.

    :returns: True if there's an update available. False if up to date."""
    pypi_url = "https://pypi.org/pypi/eldonationtracker/json"
    pypi_version = get_pypi_version(pypi_url)
    if pypi_version == "Error":
        return False
    else:
        return update_available(pypi_version, pkg_current_version)


if __name__ == "__main__":  # pragma: no cover
    main()
