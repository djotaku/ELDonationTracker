"""A class to hold the Donation attributes and methods."""


class Donation:
    """Donation Attributes.

    Class exists to provide attributes for a donation based on what comes in
    from the JSON so that it doesn't have to be traversed each time a donor
    action needs to be taken.

    :param name: the name of the donor for this donation. If the donor wished\
    to stay anonymous, the variable is set to "Anonymous"
    :type name: str

    :param message: the message associated with the donation.
    :type message: str

    :param amount: the amount of the donation. If they blocked it from showing\
    it is set to 0.
    :type amount: int
    """

    def __init__(self, name, message, amount, donor_id, avatar_url, donation_date, donation_id):
        """Load in values from class initialization."""
        if name is not None:
            self.name = name
        else:
            self.name = "Anonymous"
        self.message = message
        if amount is not None:
            self.amount = amount
        else:
            self.amount = 0
        self.donor_id: str = donor_id
        self.avatar_url: str = avatar_url
        self.donation_date: str = donation_date
        self.donation_id: str = donation_id

    def get_amount(self):
        return self.amount

    def __eq__(self, other):
        """Donation equal comparison.

        :returns: True if this donation has the same donation ID.
        """
        return self.donation_id == other.donation_id

    def __str__(self):
        return f"A donation by {self.name} in the amount of ${self.amount} with the message '{self.message}'"
