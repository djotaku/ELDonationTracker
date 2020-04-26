from eldonationtracker import donor as donor


class TeamParticipant(donor.Donor):
    """Participant Attributes.

    Inherits from the donor class, but
    over-rides the json_to_attributes function.

    API variables:

    :param self.name: participant's name or Anonymous
    :param self.amount: the sum of all donations by this participant
    :param self.number_of_donations: number of all donations by this participant
    :param self.image_url: the url of the participant's avatar image (not used)
    """

    def __init__(self, json):
        self.name, self.amount, self.number_of_donations, self.image_url = self.json_to_attributes(json)

    def json_to_attributes(self, json):
        """Convert JSON to Team Participant attributes.

        :param json: JSON attributes from API
        """
        name = ""
        if json.get('displayName') is not None:
            name = json.get('displayName')
        else:
            name = "Anonymous"
        amount = float(json.get("sumDonations"))
        number_of_donations = json.get('numDonations')
        image_url = json.get('avatarImageURL')
        return name, amount, number_of_donations, image_url

    def __str__(self):
        return f"A Team Participant named {self.name} who has donated ${self.amount:.2f} to the team over {self.number_of_donations} donations."