"""A class to hold the Donation attributes and methods."""

from eldonationtracker import extralife_io as extralife_io
from rich import print


def get_donations(donations: list, donation_url: str) -> list:
    """Get the donations from the JSON and create the donation objects.

    If the API can't be reached, the same list is returned. Only new donations are added to the list at the end.

    :param donations: A list consisting of donor.Donation objects.
    :param donation_url: The URL to go to for donations.
    :returns: A list of donor.Donation objects.
    """
    donation_json = extralife_io.get_json(donation_url)
    if not donation_json:
        print("[bold red]Couldn't access donation page[/bold red]")
        return donations
    else:
        donation_list = [Donation(donation_json[this_donation].get('displayName'),
                                  donation_json[this_donation].get('message'),
                                  donation_json[this_donation].get('amount'),
                                  donation_json[this_donation].get('donorID'),
                                  donation_json[this_donation].get('avatarImageURL'),
                                  donation_json[this_donation].get('createdDateUTC'),
                                  donation_json[this_donation].get('donationID'))
                         for this_donation in range(0, len(donation_json))]
        if len(donations) == 0:
            return donation_list
        else:
            for a_donation in reversed(donation_list):
                if a_donation not in donations:
                    donations.insert(0, a_donation)
            return donations


def format_donation_information_for_output(donation_list: list, currency_symbol: str, donors_to_display: str,
                                           team: bool) -> dict:
    """Format the donation attributes for the output files."""
    donation_formatted_output: dict = {}
    if team:
        prefix = "Team_"
    else:
        prefix = ''

    donation_formatted_output[f'{prefix}LastDonationNameAmnt'] = extralife_io.single_format(donation_list[0],
                                                                                            False, currency_symbol)
    donation_formatted_output[f'{prefix}lastNDonationNameAmts'] = \
        extralife_io.multiple_format(donation_list, False, False, currency_symbol, int(donors_to_display))
    donation_formatted_output[f'{prefix}lastNDonationNameAmtsMessage'] = \
        extralife_io.multiple_format(donation_list, True, False, currency_symbol, int(donors_to_display))
    donation_formatted_output[f'{prefix}lastNDonationNameAmtsMessageHorizontal'] = \
        extralife_io.multiple_format(donation_list, True, True, currency_symbol, int(donors_to_display))
    donation_formatted_output[f'{prefix}lastNDonationNameAmtsHorizontal'] = \
        extralife_io.multiple_format(donation_list, False, True, currency_symbol, int(donors_to_display))
    return donation_formatted_output


class Donation:
    """Donation Attributes.

    Class exists to provide attributes for a donation based on what comes in from the JSON so that it doesn't have to be
     traversed each time a donor action needs to be taken.

    :param name: the name of the donor for this donation.
    :type name: str
    :param message: the message associated with the donation.
    :type message: str
    :param amount: the amount of the donation.
    :type amount: int
    :param donor_id: the donor drive ID of the donor who made this donation
    :type donor_id: str
    :param avatar_url: the URL of the avatar associated with this donation.
    :type avatar_url: str
    :param donation_date: the date of the donation.
    :type donation_date: str
    :param donation_id: The donor drive ID of this donation
    :type donation_id: str
    """

    def __init__(self, name, message, amount, donor_id, avatar_url, donation_date, donation_id):
        """Load in values from class initialization."""
        if name is not None:
            self._name = name
        else:
            self._name = "Anonymous"
        self._message = message
        if amount is not None:
            self._amount = amount
        else:
            self._amount = 0
        self._donor_id: str = donor_id
        self._avatar_url: str = avatar_url
        self._donation_date: str = donation_date
        self._donation_id: str = donation_id

    @property
    def name(self) -> str:
        """the name of the donor for this donation. If the donor wished to stay anonymous, the variable is set to/
     'Anonymous'"""
        return self._name

    @property
    def message(self) -> str:
        """the message associated with the donation."""
        return self._message

    @property
    def amount(self) -> int:
        """the amount of the donation. If they blocked it from showing it is set to 0."""
        return self._amount

    @property
    def donor_id(self) -> str:
        """the donor drive ID of the donor who made this donation"""
        return self._donor_id

    @property
    def avatar_url(self) -> str:
        """the URL of the avatar associated with this donation."""
        return self._avatar_url

    @property
    def donation_date(self) -> str:
        """the date of the donation."""
        return self._donation_date

    @property
    def donation_id(self) -> str:
        """The donor drive ID of this donation."""
        return self._donation_id

    def __eq__(self, other):
        """Donation equal comparison.

        :returns: True if this donation has the same donation ID.
        """
        return self.donation_id == other.donation_id

    def __str__(self):
        return f"A donation by {self.name} in the amount of ${self.amount} with the message '{self.message}'"
