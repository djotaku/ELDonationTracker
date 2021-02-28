"""A donor."""


class Donor:
    """Donor Attributes.

    Class exists to provide attributes for a donor based on what comes in from
    the JSON so that it doesn't have to be traversed each time a donor action
    needs to be taken.
    """

    def __init__(self, json):
        """Load in values from class initialization.


        :param json: JSON attributes from the API
        :type json: json
        """
        self._name, self._donor_id, self._image_url, self._amount, self._number_of_donations =\
            self.json_to_attributes(json)

    @property
    def name(self) -> str:
        """Donor's name if provided, else Anonymous."""
        return self._name

    @property
    def donor_id(self) -> str:
        """The ID assigned by the API (currently not used)."""
        return self._donor_id

    @property
    def image_url(self) -> str:
        """The URL for the donor's avatar (currently not used)"""
        return self._image_url

    @property
    def amount(self) -> float:
        """The sum of all donations the donor has made this campaign"""
        return self._amount

    @property
    def number_of_donations(self) -> str:
        """The number of donations the donor has made this campaign"""
        return self._number_of_donations

    @staticmethod
    def json_to_attributes(json_values):
        """Convert API JSON values to Donor attributes.

        :param json_values: JSON attributes from the API
        :type json_values: json
        """
        if json_values.get('displayName') is not None:
            name = json_values.get('displayName')
        else:
            name = "Anonymous"
        donor_id = json_values.get('donorID')
        image_url = json_values.get('avatarImageURL')
        amount = float(json_values.get('sumDonations'))
        number_of_donations = json_values.get('numDonations')
        return name, donor_id, image_url, amount, number_of_donations

    def __lt__(self, other):
        """Donor less than comparison.

        Returns True if this Donor has a donation amount less than comparison.
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
