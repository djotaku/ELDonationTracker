class Donation:
    """Donation Attributes.

    Class exists to provide attributes for a donation based on what comes in
    from the JSON so that it doesn't have to be traversed each time a donor
    action needs to be taken.
    """

    def __init__(self, name, message, amount):
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

    def __lt__(self, object):
        """Donation less than comparison.

        Returns True if this donation has a donation
        amount less than comparision.
        """
        return self.amount < object.amount
