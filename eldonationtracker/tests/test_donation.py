"""Test methods in donor class."""

from eldonationtracker.api import donation

donation1_json = {"displayName": "Donor 1", "participantID": '4939d', "amount": 34.51, "donorID": "FAKE3C59D235B4DA",
                  "avatarImageURL": "//image.png", "message": "Good job!",
                  "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                  "donationID": "861A3C59D235B4DB"}
donation1 = donation.Donation(donation1_json)

donation2_json = {"displayName": "Donor 1", "participantID": '4939d', "amount": 34.50, "donorID": "FAKE3C59D235B4DA",
                  "avatarImageURL": "//image.png",
                  "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                  "donationID": "861A3C59D235B4DC"}
donation2 = donation.Donation(donation2_json)
donation2_equal = donation.Donation(donation1_json)

donation_anonymous_json = {"displayName": None, "participantID": '4939d', "amount": 34.51, "message": "Good job!",
                           "donorID": "FAKE3C59D235B4DA", "avatarImageURL": "//image.png",
                           "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                           "donationID": "861A3C59D235B4DD"}
donation_anonymous = donation.Donation(donation_anonymous_json)

donation_no_money_json = {"displayName": "Donor 1", "participantID": '4939d', "amount": None, "message": "Good job!",
                          "donorID": "FAKE3C59D235B4DA", "avatarImageURL": "//image.png",
                          "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                          "donationID": "861A3C59D235B4DE"}
donation_no_money = donation.Donation(donation_no_money_json)

donation1_whole_dollar_json = {"displayName": "Donor 1", "participantID": '4939d', "amount": 34,
                               "donorID": "FAKE3C59D235B4DA", "avatarImageURL": "//image.png",
                               "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                               "donationID": "861A3C59D235B4DF"}
donation1_whole_dollar = donation.Donation(donation1_whole_dollar_json)

donation2_whole_dollar_json = {"displayName": "Donor 1", "participantID": '4939d', "amount": 32,
                               "donorID": "FAKE3C59D235B4DA", "avatarImageURL": "//image.png",
                               "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                               "donationID": "861A3C59D235B4DG"}
donation2_whole_dollar = donation.Donation(donation2_whole_dollar_json)

fake_participant_info = {'sumDonations': 500, 'numDonations': 5, 'fundraisingGoal': 1000}
fake_donations = {"displayName": "Sean Gibson", "participantID": 401280, "amount": 25.00, "donorID": "54483486D840B7EA",
                  "avatarImageURL": "//assets.donordrive.com/clients/extralife/img/avatar-constituent-default.gif",
                  "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                  "donationID": "861A3C59D235B4DA"}, {"displayName": "Eric Mesa", "participantID": 401280,
                                                      "amount": 25.00, "donorID": "4162ECD2B8BF4C17",
                                                      "avatarImageURL": "//assets.donordrive.com/extralife/images/$avat"
                                                                        "ars$/constituent_D4DC394A-C293-34EB-4162ECD2B"
                                                                        "8BF4C17.jpg",
                                                      "createdDateUTC": "2020-01-05T20:35:28.897+0000",
                                                      "eventID": 547, "teamID": 50394, "donationID": "7D430E9E9AF79686"}
donation_emoji_json = {"displayName": "🍀🍀🍀🍀", "participantID": '4939d', "amount": 34.51,
                       "donorID": "FAKE3C59D235B4DA", "avatarImageURL": "//image.png", "message": "Good job!",
                       "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                       "donationID": "861A3C59D235B4DA"}


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
    assert donation2_whole_dollar.amount < donation1_whole_dollar.amount


def test_donation_lt_change():
    """Test to make sure comparison works.

    Uses dollars and cents.
    """
    assert donation2.amount < donation1.amount


def test_donation_equal():
    """Test to make sure comparison works.

    This time they're equal.
    """
    assert donation2_equal.amount == donation1.amount


def test_donation_str():
    """Test that the class string is properly created."""
    assert str(donation1) == "A donation by Donor 1 in the amount of $34.51 with the message 'Good job!'"


def test_emoji_in_donor_name():
    """Test that an emoji in the donor name will not crash things."""
    emoji_donation = donation.Donation(donation_emoji_json)
    assert emoji_donation.name == "🍀🍀🍀🍀"
    assert str(emoji_donation) == "A donation by 🍀🍀🍀🍀 in the amount of $34.51 with the message 'Good job!'"