from eldonationtracker.utils import update_available


def test_local_major_version_old():
    """Test to make sure if the major version on PyPi is higher,\
    it returns True."""
    pypi_version = "2.0.0"
    pkg_current_version = "1.0.0"
    update = update_available.update_available(pypi_version,
                                               pkg_current_version)
    assert update


def test_local_minor_version_old():
    """Test to make sure if the minor version on PyPi is higher,\
    it returns True."""
    pypi_version = "2.1.0"
    pkg_current_version = "2.0.1"
    update = update_available.update_available(pypi_version,
                                               pkg_current_version)
    assert update


def test_local_patch_version_old():
    """Test to make sure if the patch version on PyPi is higher,\
    it returns True."""
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
