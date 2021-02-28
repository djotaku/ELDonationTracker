"""A class to hold the Donation attributes and methods."""


class Donation:
    """Donation Attributes.

    Class exists to provide attributes for a donation based on what comes in from the JSON so that it doesn't have to be
     traversed each time a donor action needs to be taken.
    """

    def __init__(self, json):
        """Load in values from class initialization.

        :param json: JSON attributes from the API
        :type json: json
        """
        self._name, self._message, self._amount, self._donor_id, self._avatar_url, self._donation_date,\
            self._donation_id = self.json_to_attributes(json)

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

    @staticmethod
    def json_to_attributes(json):
        """Convert API JSON values to Donation attributes.

        :param json: JSON attributes from the API
        :type json: json
        """
        if json.get('displayName') is not None:
            name = json.get('displayName')
        else:
            name = "Anonymous"
        message = json.get('message')
        amount = json.get('amount') if json.get('amount') is not None else 0
        donor_id = json.get('donorID')
        avatar_url = json.get('avatarImageURL')
        donation_date = json.get('createdDateUTC')
        donation_id = json.get('donationID')
        return name, message, amount, donor_id, avatar_url, donation_date, donation_id

    def __eq__(self, other):
        """Donation equal comparison.

        :returns: True if this donation has the same donation ID.
        """
        return self.donation_id == other.donation_id

    def __str__(self):
        return f"A donation by {self.name} in the amount of ${self.amount} with the message '{self.message}'"
