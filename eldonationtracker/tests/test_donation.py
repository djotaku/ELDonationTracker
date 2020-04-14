"""Test methods in donor class."""

from eldonationtracker import donation

donation1 = donation.Donation("Donor 1", "Good job!", 34.51, "4939d", "http://image.png",
                              "2020-02-11T17:22:23.963+0000", "861A3C59D235B4DA")

donation2 = donation.Donation("Donor 1", "Good job!", 34.50, "4939d", "http://image.png",
                              "2020-02-11T17:22:23.963+0000", "861A3C59D235B4DA")

donation2_equal = donation.Donation("Donor 1", "Good job!", 34.51, "4939d", "http://image.png",
                                    "2020-02-11T17:22:23.963+0000", "861A3C59D235B4DA")

donation_anonymous = donation.Donation(None, "Good job!", 34.51, "4939d", "http://image.png",
                                       "2020-02-11T17:22:23.963+0000", "861A3C59D235B4DA")

donation_no_money = donation.Donation("Donor 1", "Good job!", None, "4939d", "http://image.png",
                                      "2020-02-11T17:22:23.963+0000", "861A3C59D235B4DA")

donation1_whole_dollar = donation.Donation("Donor 1", "Good job!", 34, "4939d", "http://image.png",
                                           "2020-02-11T17:22:23.963+0000", "861A3C59D235B4DA")

donation2_whole_dollar = donation.Donation("Donor 1", "Good job!", 32, "4939d", "http://image.png",
                                           "2020-02-11T17:22:23.963+0000", "861A3C59D235B4DA")


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
    assert donation2_whole_dollar < donation1_whole_dollar


def test_donation_lt_change():
    """Test to make sure comparison works.

    Uses dollars and cents.
    """
    assert donation2 < donation1


def test_donation_equal():
    """Test to make sure comparison works.

    This time they're equal.
    """
    assert donation2_equal == donation1


def test_donation_str():
    """Test that the class string is properly created."""
    assert str(donation1) == "A donation by Donor 1 in the amount of $34.51 with the message 'Good job!'"
