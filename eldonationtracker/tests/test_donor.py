"""Test methods in donor class."""

from eldonationtracker.api import donor


def test_donor_attributes_none_missing():
    donor1_json = {"displayName": "donor1", "sumDonations": "45", "donorID": 1000111,
                   'avatarImageURL': "http://someplace.com/image.jpg", "numDonations": 2}
    donor1 = donor.Donor(donor1_json)
    assert donor1.name == "donor1"
    assert donor1.donor_id == 1000111
    assert donor1.image_url == "http://someplace.com/image.jpg"
    assert donor1.amount == 45
    assert donor1.number_of_donations == 2


def test_donor_attributes_name_missing():
    donor1_json = {"sumDonations": "45", "donorID": 1000111,
                   'avatarImageURL': "http://someplace.com/image.jpg", "numDonations": 2}
    donor1 = donor.Donor(donor1_json)
    assert donor1.name == "Anonymous"
    assert donor1.donor_id == 1000111
    assert donor1.image_url == "http://someplace.com/image.jpg"
    assert donor1.amount == 45
    assert donor1.number_of_donations == 2


def test_donor_lt_whole_numbers():
    """Test to make sure comparison works.

    Uses whole dollar amounts.
    """
    donor1_json = {"displayName": "donor1", "sumDonations": "45"}
    donor2_json = {"displayName": "donor2", "sumDonations": "30"}
    donor1 = donor.Donor(donor1_json)
    donor2 = donor.Donor(donor2_json)
    assert donor2 < donor1


def test_donor_lt_change():
    """Test to make sure comparison works.

    Uses dollars and cents.
    """
    donor1_json = {"displayName": "donor1", "sumDonations": "30.00"}
    donor2_json = {"displayName": "donor2", "sumDonations": "30.01"}
    donor1 = donor.Donor(donor1_json)
    donor2 = donor.Donor(donor2_json)
    assert donor1 < donor2


def test_donors_equal():
    """Test to make sure comparison works.

    This time they're equal.
    """
    donor1_json = {"displayName": "donor1", "sumDonations": "30"}
    donor2_json = {"displayName": "donor2", "sumDonations": "30"}
    donor1 = donor.Donor(donor1_json)
    donor2 = donor.Donor(donor2_json)
    assert donor1 == donor2


def test_str():
    donor1_json = {"displayName": "donor1", "sumDonations": "45", "donorID": 1000111,
                   'avatarImageURL': "http://someplace.com/image.jpg", "numDonations": 2}
    donor1 = donor.Donor(donor1_json)
    assert str(donor1) == "A donor named donor1 with donor ID 1000111 who has donated $45.00 over 2 donations."


def test_emoji_in_name():
    """Test to make sure that emoji in the donor's name doesn't crash the program."""
    emoji_donor_json = {"displayName": "🍀🍀🍀🍀", "sumDonations": "45", "donorID": 1000111,
                   'avatarImageURL': "http://someplace.com/image.jpg", "numDonations": 2}
    emoji_donor = donor.Donor(emoji_donor_json)
    assert emoji_donor.name == "🍀🍀🍀🍀"
