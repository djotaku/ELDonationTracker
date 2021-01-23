"""A donor."""


class Donor:
    """Donor Attributes.

    Class exists to provide attributes for a donor based on what comes in from
    the JSON so that it doesn't have to be traversed each time a donor action
    needs to be taken.

    :param json: JSON attributes from the API
    :type json: json
    :param self._name: donor's name if provided, else Anonymous
    :type self._name: str
    :param self._donor_id: the ID assigned by the API (currently not used)
    :type self._donor_id: str
    :param self._image_url: the URL for the donor's avatar (currently not used)
    :type self._image_url: str
    :param self._amount: the sum of all donations the donor has made this campaign
    :type self._amount: float
    :param self._number_of_donations: the number of donations the donor has made this campaign
    :type self._number_of_donations: str
    """

    def __init__(self, json):
        """Load in values from class initialization."""
        self._name, self._donor_id, self._image_url, self._amount, self._number_of_donations =\
            self.json_to_attributes(json)

    @property
    def name(self):
        return self._name

    @property
    def donor_id(self):
        return self._donor_id

    @property
    def image_url(self):
        return self._image_url

    @property
    def amount(self):
        return self._amount

    @property
    def number_of_donations(self):
        return self._number_of_donations

    @staticmethod
    def json_to_attributes(json):
        """Convert API JSON values to Donor attributes.

        :param json: JSON attributes from the API
        :type json: json
        """
        name = ""
        if json.get('displayName') is not None:
            name = json.get('displayName')
        else:
            name = "Anonymous"
        donor_id = json.get('donorID')
        image_url = json.get('avatarImageURL')
        amount = float(json.get('sumDonations'))
        number_of_donations = json.get('numDonations')
        return name, donor_id, image_url, amount, number_of_donations

    def __lt__(self, other):
        """Donor less than comparison.

        Returns True if this Donor has a donation
        amount less than comparision.
        """
        return self.amount < other.amount

    def __eq__(self, other):
        """Donor equal comparison.

        Returns True if this Donor and the other have the same amount.
        """
        return self.amount == other.amount

    def __str__(self):
        """Returns a string representation of this donor."""
        return f"A donor named {self.name} with donor ID {self.donor_id} who has donated ${self.amount:.2f}"\
               f" over {self.number_of_donations} donations."
