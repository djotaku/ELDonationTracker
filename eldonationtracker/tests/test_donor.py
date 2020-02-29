"""Test methods in donor class."""

from eldonationtracker import donor


def test_Donor_lt_whole_numbers():
    """Test to make sure comparison works.

    Uses whole dollar amounts.
    """
    donor1_json = {"displayName": "donor1", "sumDonations": "45"}
    donor2_json = {"displayName": "donor2", "sumDonations": "30"}
    donor1 = donor.Donor(donor1_json)
    donor2 = donor.Donor(donor2_json)
    assert donor2 < donor1


def test_Donor_lt_change():
    """Test to make sure comparison works.

    Uses dollars and cents.
    """
    donor1_json = {"displayName": "donor1", "sumDonations": "30.00"}
    donor2_json = {"displayName": "donor2", "sumDonations": "30.01"}
    donor1 = donor.Donor(donor1_json)
    donor2 = donor.Donor(donor2_json)
    assert donor1 < donor2


def test_Donors_equal():
    """Test to make sure comparison works.

    This time they're equal.
    """
    donor1_json = {"displayName": "donor1", "sumDonations": "30"}
    donor2_json = {"displayName": "donor2", "sumDonations": "30"}
    donor1 = donor.Donor(donor1_json)
    donor2 = donor.Donor(donor2_json)
    assert donor1 == donor2
