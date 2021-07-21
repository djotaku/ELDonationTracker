"""Return true if there is an update available.

An update is available if the version on PyPi is higher than the version the user has on their machine.
"""

import json
import logging
from rich.logging import RichHandler
import semver  # type: ignore
import ssl
from urllib.request import Request, urlopen  # type: ignore
from urllib.error import HTTPError, URLError  # type: ignore

from eldonationtracker import __version__ as pkg_current_version

# logging
LOG_FORMAT = '%(name)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, handlers=[RichHandler(markup=True, show_path=False)])
update_log = logging.getLogger("update available")


def get_pypi_version(url: str) -> str:
    """Use PyPi JSON API to get latest version.

    :return: A string with the version number.
    """
    context = ssl._create_unverified_context()
    this_program_json: dict = {}
    try:
        request = Request(url=url)
        payload = urlopen(request, timeout=5, context=context)
        this_program_json = json.load(payload)
    except (HTTPError, URLError):
        update_log.error("Could not get JSON")
        return "Error"
    return this_program_json["info"]["version"]


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
