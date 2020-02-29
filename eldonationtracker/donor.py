"""A donor."""


class Donor:
    """Donor Attributes.

    Class exists to provide attributes for a donor based on what comes in from
    the JSON so that it doesn't have to be traversed each time a donor action
    needs to be taken.

    :param json: JSON attributes from the API
    :type json: json
    :param name: donor's name if provided, else Anonymous
    :type name: str
    :param donor_id: the ID assigned by the API (currently not used)
    :type donor_id: str
    :param image_url: the URL for the donor's avatar (currently not used)
    :type image_url: str
    :param amount: the sum of all donations the donor has made this\
    campaign number_of_dononations: the number of donations the donor has\
    made this campaign
    """

    def __init__(self, json):
        """Load in values from class initialization."""
        self.json_to_attributes(json)

    def json_to_attributes(self, json):
        """Convert API JSON values to Donor attributes.

        May be overwritten by child classes.

        :param json: JSON attributes from the API
        :type json: json
        """
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

    def __eq__(self, object):
        """Donor equal comparison.

        Returns True if thid Donor and the other have the same amount.
        """
        return self.amount == object.amount
