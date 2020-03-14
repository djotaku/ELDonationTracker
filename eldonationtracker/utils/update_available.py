"""Return true if there is an update available.

An update is available if the version on PyPi is higher than the \
version the user has on their machine.
"""

import json
import semver  # type: ignore
import ssl
from urllib.request import HTTPError, Request, URLError, urlopen  # type: ignore

from eldonationtracker import __version__ as pkg_current_version


def get_pypi_version() -> str:
    """Use PyPi JSON API to get latest version.

    :return: A string with the version number.
    """
    url = "https://pypi.org/pypi/eldonationtracker/json"
    context = ssl._create_unverified_context()
    eldt_json: dict
    try:
        request = Request(url=url)
        payload = urlopen(request, timeout=5, context=context)
        eldt_json = json.load(payload)
    except HTTPError:
        print("Could not get JSON")
    return(eldt_json["info"]["version"])


def update_available(pypi_version: str, current_version: str) -> bool:
    """Use semver module to calculate whether there is a newer version on PyPi.

    :return: True if the PyPi version is higer than the version being run.\
    Returns false if the version being compared to PyPi is equal or greater\
    than the PyPi version."""
    if semver.compare(pypi_version, current_version) == 1:
        print(f"There is an update available. PyPi version: {pypi_version}")
        return True
    else:
        print("You have the latest version.")
        return False


def main():
    pypi_version = get_pypi_version()
    result = update_available(pypi_version, pkg_current_version)
    return result


if __name__ == "__main__":
    main()
