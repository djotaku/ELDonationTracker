from unittest import mock

from eldonationtracker.utils import update_available

fake_py_pi_json = {"info": {"version": "4.4.4"}}
fake_url_json_load = mock.Mock()
fake_url_json_load.return_value = fake_py_pi_json


@mock.patch.object(update_available.json, "load", fake_url_json_load)
def test_get_pypi_version():
    version = update_available.get_pypi_version("https://pypi.org/pypi/eldonationtracker/json")
    assert version == "4.4.4"


def test_get_pypi_version_exception():
    version = update_available.get_pypi_version("https://pypi.org/pypi/eldonationtracker_wrong/json")
    assert version == "Error"


def test_local_major_version_old():
    """Test to make sure if the major version on PyPi is higher, it returns True."""
    pypi_version = "2.0.0"
    pkg_current_version = "1.0.0"
    update = update_available.update_available(pypi_version,
                                               pkg_current_version)
    assert update


def test_local_minor_version_old():
    """Test to make sure if the minor version on PyPi is higher, it returns True."""
    pypi_version = "2.1.0"
    pkg_current_version = "2.0.1"
    update = update_available.update_available(pypi_version,
                                               pkg_current_version)
    assert update


def test_local_patch_version_old():
    """Test to make sure if the patch version on PyPi is higher, it returns True."""
    pypi_version = "2.0.1"
    pkg_current_version = "2.0.0"
    update = update_available.update_available(pypi_version,
                                               pkg_current_version)
    assert update


def test_up_to_date_major():
    """Test to make sure if the version is up to date, it returns false."""
    pypi_version = "2.0.0"
    pkg_current_version = "2.0.0"
    update = update_available.update_available(pypi_version,
                                               pkg_current_version)
    assert update is False


def test_up_to_date_minor():
    """Test to make sure if the version is up to date, it returns false."""
    pypi_version = "2.1.0"
    pkg_current_version = "2.1.0"
    update = update_available.update_available(pypi_version,
                                               pkg_current_version)
    assert update is False


def test_up_to_date_patch():
    """Test to make sure if the version is up to date, it returns false."""
    pypi_version = "2.1.1"
    pkg_current_version = "2.1.1"
    update = update_available.update_available(pypi_version,
                                               pkg_current_version)
    assert update is False


fake_get_pypi_version_error = mock.Mock()
fake_get_pypi_version_error.return_value = "Error"


@mock.patch.object(update_available, "get_pypi_version", fake_get_pypi_version_error)
def test_main_error():
    result = update_available.main()
    assert result is False


fake_get_pypi_version = mock.Mock()
fake_get_pypi_version.return_value = "4.4.4"


@mock.patch.object(update_available, "get_pypi_version", fake_get_pypi_version)
def test_main_time_to_update():
    update_available.pkg_current_version = "2.1.0"
    result = update_available.main()
    assert result is True


@mock.patch.object(update_available, "get_pypi_version", fake_get_pypi_version)
def test_main_already_up_to_date():
    update_available.pkg_current_version = "4.4.4"
    result = update_available.main()
    assert result is False
