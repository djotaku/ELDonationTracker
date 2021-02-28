from eldonationtracker.api import donor as donor


class TeamParticipant(donor.Donor):
    """Participant Attributes.

    Inherits from the donor class, but
    over-rides the json_to_attributes function.

    API variables:

    :param self.name: participant's name
    :param self.amount: the sum of all donations by this participant
    :param self.number_of_donations: number of all donations by this participant
    :param self.image_url: the url of the participant's avatar image (not used)
    """

    def __str__(self):
        return f"A Team Participant named {self.name} who has donated ${self.amount:.2f} to the team over" \
               f" {self.number_of_donations} donations."
