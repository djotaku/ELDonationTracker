"""A donor."""

class Donor:
    """Donor Attributes.

    Class exists to provide attributes for a donor based on what comes in from
    the JSON so that it doesn't have to be traversed each time a donor action
    needs to be taken.
    """

    def __init__(self, json):
        """Load in values from class initialization."""
        self.json_to_attributes(json)

    def json_to_attributes(self, json):
        """Convert JSON to Donor attributes.

        May be overwritten by child classes."""
        if json.get('displayName') is not None:
            self.name = json.get('displayName')
        else:
            self.name = "Anonymous"
        self.donor_id = json.get('donorID')
        self.image_url = json.get('avatarImageURL')
        self.amount = float(json.get('sumDonations'))
        self.number_of_dononations = json.get('numDonations')

    def __lt__(self, object):
        """Donor less than comparison.

        Returns True if this Donor has a donation
        amount less than comparision.
        """
        return self.amount < object.amount