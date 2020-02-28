"""Return true if there is an update available.

An update is available if the version on PyPi is higher than the\
version the user has on their machine.
"""

import json
import semver
from urllib.request import HTTPError, Request, URLError, urlopen

from eldonationtracker import __version__ as current_version


def get_pypi_version() -> str:
    """Use PyPi JSON API to get latest version.

    :return: A string with the version number.
    """
    url = "https://pypi.org/pypi/eldonationtracker/json"
    eldt_json: dict
    try:
        request = Request(url=url)
        payload = urlopen(request, timeout=5)
        eldt_json = json.load(payload)
    except HTTPError:
        print("Could not get JSON")
    return(eldt_json["info"]["version"])


def update_available() -> bool:
    pypi_version = get_pypi_version()
    if semver.compare(pypi_version, current_version) == 1:
        return True
    else:
        return False


def main():
    result = update_available()
    print(result)


if __name__ == "__main__":
    main()
