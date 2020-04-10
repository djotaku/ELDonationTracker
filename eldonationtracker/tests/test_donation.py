"""Test methods in donor class."""

from eldonationtracker import donation


def test_donation_attributes_no_blanks():
    """Test to make sure attributes are properly assigned."""
    donation1 = donation.Donation("Donor 1", "Good job!", 34.51)
    assert donation1.name == "Donor 1"
    assert donation1.message == "Good job!"
    assert donation1.amount == 34.51


def test_donation_attributes_no_name():
    """Test to make sure attributes are properly assigned."""
    donation1 = donation.Donation(None, "Good job!", 34.51)
    assert donation1.name == "Anonymous"
    assert donation1.message == "Good job!"
    assert donation1.amount == 34.51


def test_donation_attributes_no_amount():
    """Test to make sure attributes are properly assigned."""
    donation1 = donation.Donation("Donor 1", "Good job!", None)
    assert donation1.name == "Donor 1"
    assert donation1.message == "Good job!"
    assert donation1.amount == 0


def test_donation_lt_whole_numbers():
    """Test to make sure comparison works.

    Uses whole dollar amounts.
    """
    donation1 = donation.Donation("Donor 1", "Good job!", 34)
    donation2 = donation.Donation("Donor 1", "Good job!", 32)
    assert donation2 < donation1


def test_donation_lt_change():
    """Test to make sure comparison works.

    Uses dollars and cents.
    """
    donation1 = donation.Donation("Donor 1", "Good job!", 34.51)
    donation2 = donation.Donation("Donor 1", "Good job!", 34.50)
    assert donation2 < donation1


def test_donation_equal():
    """Test to make sure comparison works.

    This time they're equal.
    """
    donation1 = donation.Donation("Donor 1", "Good job!", 34.51)
    donation2 = donation.Donation("Donor 1", "Good job!", 34.51)
    assert donation2 == donation1


def test_donation_str():
    """Test that the class string is properly created."""
    donation1 = donation.Donation("Donor 1", "Good job!", 34.51)
    assert str(donation1) == "A donation by Donor 1 in the amount of $34.51 with the message 'Good job!'"
