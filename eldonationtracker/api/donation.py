"""A class to hold the Donation attributes and methods."""


class Donation:
    """Donation Attributes.

    Class exists to provide attributes for a donation based on what comes in from the JSON so that it doesn't have to be
     traversed each time a donor action needs to be taken.
    """

    def __init__(self, name, message, amount, donor_id, avatar_url, donation_date, donation_id):
        """Load in values from class initialization.

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
        :type donation_id: str"""
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
