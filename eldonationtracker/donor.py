"""A donor."""


class Donor:
    """Donor Attributes.

    Class exists to provide attributes for a donor based on what comes in from
    the JSON so that it doesn't have to be traversed each time a donor action
    needs to be taken.

    :param json: JSON attributes from the API
    :type json: json
    :param self.name: donor's name if provided, else Anonymous
    :type name: str
    :param self.donor_id: the ID assigned by the API (currently not used)
    :type donor_id: str
    :param self.image_url: the URL for the donor's avatar (currently not used)
    :type image_url: str
    :param self.amount: the sum of all donations the donor has made this campaign
    :param self.number_of_donations: the number of donations the donor has made this campaign
    """

    def __init__(self, json):
        """Load in values from class initialization."""
        self.name, self.donor_id, self.image_url, self.amount, self.number_of_donations = self.json_to_attributes(json)

    def json_to_attributes(self, json):
        """Convert API JSON values to Donor attributes.

        May be overwritten by child classes.

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

    # for __lt__ and __eq__ probably want to do similar to donation.py
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
