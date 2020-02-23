"""Test methods in donor class."""

from eldonationtracker import donor

donor1_json = {"displayName": "donor1", "sumDonations": "45"}
donor2_json = {"displayName": "donor2", "sumDonations": "30"}

def test_Donor_lt():
    """ Test to make sure comparison works. """
    donor1 = donor.Donor(donor1_json)
    donor2 = donor.Donor(donor2_json)
    assert donor2 < donor1
