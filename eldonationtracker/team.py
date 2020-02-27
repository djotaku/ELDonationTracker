"""Contains classes pertaining to teams."""
from eldonationtracker import donor as donor
from eldonationtracker import extralife_IO as extralife_IO


class Team:
    """Hold Team Data."""

    def __init__(self, team_id, folder, currency_symbol):
        """Set the team variables.

        API Variables:
        team_url and team_participant_url: self-explanatory
        team_info: a dictionary to hold the following:
                   - Team_goal: fundraising goal
                   - Team_captain: team captain's name
                   - Team_totalRaised: total amount raised by team
                   - Team_numDonations: total number of donations to the team
        participant_list: a list of the most recent participants
        top_5_participant_list: a list of the top 5 team participants by
                                amount donated.

        Helper Variables:
        output_folder: the folder that will contain the txt files for the user
                       (comes in via the init function from the participant)
        currency_symbol: for formatting text (comes in via init function)
        participant_calculation_dict: dictionary holding output for txt files:
                   - Team_Top5Participants: top 5 participants by
                     donation amount
                   - Team_Top5ParticipantsHorizontal: same, but horizontal
                   - Team_TopParticipantNameAmnt: Top participant and amount
        """
        # urls
        team_url_base = "https://www.extra-life.org/api/teams/"
        self.team_url = f"{team_url_base}{team_id}"
        self.team_participant_url = f"{team_url_base}{team_id}/participants"
        # misc
        self.output_folder = folder
        self.currency_symbol = currency_symbol
        self.team_info = {}
        self.participant_calculation_dict = {}
        self.top_5_participant_list = []

    def get_team_json(self):
        """Get team info from JSON api."""
        # need to debug to keep program from exiting if it can't read the URL
        self.team_json = extralife_IO.get_JSON(self.team_url)
        if self.team_json == 0:
            print("Could not get team JSON")
        else:
            self.team_goal = self.team_json["fundraisingGoal"]
            self.team_captain = self.team_json["captainDisplayName"]
            self.total_raised = self.team_json["sumDonations"]
            self.num_donations = self.team_json["numDonations"]
            # dictionary
            self.team_info["Team_goal"] = f"{self.currency_symbol}{self.team_goal:,.2f}"
            self.team_info["Team_captain"] = f"{self.team_captain}"
            self.team_info["Team_totalRaised"] = f"{self.currency_symbol}{self.total_raised:,.2f}"
            self.team_info["Team_numDonations"] = f"{self.num_donations}"

    def get_participants(self):
        """Get team participants."""
        self.participant_list = []
        self.team_participant_json = extralife_IO.get_JSON(self.team_participant_url)
        if self.team_participant_json == 0:
            print("couldn't get to URL")
        elif len(self.team_participant_json) == 0:
            print("No team participants!")
        else:
            self.participant_list = [TeamParticipant(self.team_participant_json[participant]) for participant in range(0, len(self.team_participant_json))]

    def get_top_5_participants(self):
        """Get team participants."""
        self.top5_team_participant_json = extralife_IO.get_JSON(self.team_participant_url, True)
        if self.top5_team_participant_json == 0:
            print("Couldn't get top 5 team participants")
        elif len(self.top5_team_participant_json) == 0:
            print("No team participants!")
        else:
            self.top_5_participant_list = [TeamParticipant(self.top5_team_participant_json[participant]) for participant in range(0, len(self.top5_team_participant_json))]

    def _top_participant(self):
        """Get Top Team Participant.

        This should just grab element 0 from above instead of hitting API twice
        """
        if len(self.top_5_participant_list) == "0":
            print("No participants")
        else:
            return (f"{self.top_5_participant_list[0].name} - $"
                    f"{self.top_5_participant_list[0].amount:,.2f}")

    def _participant_calculations(self):
        self.participant_calculation_dict['Team_TopParticipantNameAmnt'] = self._top_participant()
        self.participant_calculation_dict['Team_Top5ParticipantsHorizontal'] = extralife_IO.multiple_format(self.top_5_participant_list, False, True, self.currency_symbol, 5)
        self.participant_calculation_dict['Team_Top5Participants'] = extralife_IO.multiple_format(self.top_5_participant_list, False, False, self.currency_symbol, 5)

    def write_text_files(self, dictionary):
        """Write info to text files."""
        extralife_IO.write_text_files(dictionary, self.output_folder)

    def team_run(self):
        """Get team info from API."""
        self.get_team_json()
        self.write_text_files(self.team_info)

    def participant_run(self):
        """Get and calculate team partipant info."""
        self.get_participants()
        self.get_top_5_participants()
        self._participant_calculations()
        self.write_text_files(self.participant_calculation_dict)


class TeamParticipant(donor.Donor):
    """Participant Attributes.

    Inherits from the donor class, but
    over-rides the json_to_attributes function.

    API variables:
    name: participant's name or Anonymous
    amount: the sum of all donations by this participant
    number_of_donations: number of all donations by this participant
    image_url: the url of the participant's avatar image (not used)
    """

    def json_to_attributes(self, json):
        """Convert JSON to Team Participant attributes."""
        if json.get('displayName') is not None:
            self.name = json.get('displayName')
        else:
            self.name = "Anonymous"
        self.amount = float(json.get("sumDonations"))
        self.number_of_donations = json.get('numDonations')
        self.image_url = json.get('avatarImageURL')


if __name__ == "__main__":
    # debug next line
    folder = "/home/ermesa/Programming Projects/python/extralife/testOutput"
    myteam = Team(44013, folder, "$")
    myteam.get_team_json()
    myteam.get_participants()
    myteam._participant_calculations()
    myteam.write_text_files(myteam.team_info)
    myteam.write_text_files(myteam.participant_calculation_dict)