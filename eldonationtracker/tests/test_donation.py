"""Test methods in donor class."""

from eldonationtracker import donation

from unittest import mock

donation1 = donation.Donation("Donor 1", "Good job!", 34.51, "4939d", "http://image.png",
                              "2020-02-11T17:22:23.963+0000", "FAKE3C59D235B4DA")

donation2 = donation.Donation("Donor 1", "Good job!", 34.50, "4939d", "http://image.png",
                              "2020-02-11T17:22:23.963+0000", "FAKE2C59D235B4DA")

donation2_equal = donation.Donation("Donor 1", "Good job!", 34.51, "4939d", "http://image.png",
                                    "2020-02-11T17:22:23.963+0000", "FAKE3C59D235B4DA")

donation_anonymous = donation.Donation(None, "Good job!", 34.51, "4939d", "http://image.png",
                                       "2020-02-11T17:22:23.963+0000", "FAKE43C59D235B4DA")

donation_no_money = donation.Donation("Donor 1", "Good job!", None, "4939d", "http://image.png",
                                      "2020-02-11T17:22:23.963+0000", "FAKE53C59D235B4DA")

donation1_whole_dollar = donation.Donation("Donor 1", "Good job!", 34, "4939d", "http://image.png",
                                           "2020-02-11T17:22:23.963+0000", "FAKE63C59D235B4DA")

donation2_whole_dollar = donation.Donation("Donor 1", "Good job!", 32, "4939d", "http://image.png",
                                           "2020-02-11T17:22:23.963+0000", "FAKE7C59D235B4DA")

fake_participant_info = {'sumDonations': 500, 'numDonations': 5, 'fundraisingGoal': 1000}
fake_donations = {"displayName": "Sean Gibson", "participantID": 401280, "amount": 25.00, "donorID":"54483486D840B7EA",
                  "avatarImageURL": "//assets.donordrive.com/clients/extralife/img/avatar-constituent-default.gif",
                  "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                  "donationID": "861A3C59D235B4DA"}, {"displayName": "Eric Mesa", "participantID": 401280,
                                                      "amount": 25.00, "donorID": "4162ECD2B8BF4C17",
                                                      "avatarImageURL": "//assets.donordrive.com/extralife/images/$avat"
                                                                        "ars$/constituent_D4DC394A-C293-34EB-4162ECD2B"
                                                                        "8BF4C17.jpg",
                                                      "createdDateUTC": "2020-01-05T20:35:28.897+0000",
                                                      "eventID": 547, "teamID": 50394, "donationID": "7D430E9E9AF79686"}

fake_extralife_io = mock.Mock()
fake_extralife_io.get_json.return_value = fake_participant_info
fake_extralife_io.get_JSON_donations.return_value = fake_donations
fake_extralife_io.get_JSON_no_json.return_value = {}
fake_extralife_io.get_JSON_donations_no_json.return_value = {}
fake_extralife_io.get_JSON_top_donor_no_json.return_value = {}


@mock.patch.object(donation.extralife_io, "get_json", fake_extralife_io.get_JSON_donations)
def test_get_donations():
    donation_list = []
    donations = donation.get_donations(donation_list, "http://fakeurl.com")
    assert donations[0].name == "Sean Gibson"
    assert donations[1].name == "Eric Mesa"


@mock.patch.object(donation.extralife_io, "get_json", fake_extralife_io.get_JSON_donations_no_json)
def test_get_donations_no_json():
    donation_list = []
    donations = donation.get_donations(donation_list, "http://fakeurl.com")
    assert donations == []


@mock.patch.object(donation.extralife_io, "get_json", fake_extralife_io.get_JSON_donations)
def test_get_donations_already_a_donation_present():
    donation_list = [donation1]
    donation_list = donation.get_donations(donation_list, "http://fakeurl.com")
    assert donation_list[0].name == "Sean Gibson"
    assert donation_list[1].name == "Eric Mesa"
    assert donation_list[2].name == "Donor 1"


def test_donation_attributes_no_blanks():
    """Test to make sure attributes are properly assigned."""
    assert donation1.name == "Donor 1"
    assert donation1.message == "Good job!"
    assert donation1.amount == 34.51


def test_donation_attributes_no_name():
    """Test to make sure attributes are properly assigned."""
    assert donation_anonymous.name == "Anonymous"
    assert donation_anonymous.message == "Good job!"
    assert donation_anonymous.amount == 34.51


def test_donation_attributes_no_amount():
    """Test to make sure attributes are properly assigned."""
    assert donation_no_money.name == "Donor 1"
    assert donation_no_money.message == "Good job!"
    assert donation_no_money.amount == 0


def test_donation_lt_whole_numbers():
    """Test to make sure comparison works.

    Uses whole dollar amounts.
    """
    assert donation2_whole_dollar.get_amount() < donation1_whole_dollar.get_amount()


def test_donation_lt_change():
    """Test to make sure comparison works.

    Uses dollars and cents.
    """
    assert donation2.get_amount() < donation1.get_amount()


def test_donation_equal():
    """Test to make sure comparison works.

    This time they're equal.
    """
    assert donation2_equal.get_amount() == donation1.get_amount()


def test_donation_str():
    """Test that the class string is properly created."""
    assert str(donation1) == "A donation by Donor 1 in the amount of $34.51 with the message 'Good job!'"
