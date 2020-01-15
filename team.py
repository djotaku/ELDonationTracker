""" Contains classes pertaining to teams."""
import extralife_IO
import donor


class Team:
    """Hold Team Data."""
    def __init__(self, team_ID, folder, currency_symbol):
        # urls
        self.team_url = f"https://www.extra-life.org/api/teams/{team_ID}"
        self.team_participant_url = f"https://www.extra-life.org/api/teams/{team_ID}/participants"
        # misc
        self.output_folder = folder
        self.currency_symbol = currency_symbol
        self.team_info = {}
        self.participant_calculation_dict = {}
        self.top_5_participant_list = []

    def get_team_json(self):
        """Get team info from JSON api."""
        self.team_json = extralife_IO.get_JSON(self.team_url)
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
        """ Get Top Team Participant. This should just grab element 0 from above instead of hitting API twice"""
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
        self.get_team_json()
        self.write_text_files(self.team_info)

    def participant_run(self):
        self.get_participants()
        self.get_top_5_participants()
        self._participant_calculations()
        self.write_text_files(self.participant_calculation_dict)


class TeamParticipant(donor.Donor):
    """Participant Attributes."""
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
