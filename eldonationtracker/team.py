"""Contains classes pertaining to teams."""
from eldonationtracker import extralife_io as extralife_io
from eldonationtracker import base_api_url
from eldonationtracker.team_participant import TeamParticipant


class Team:
    """Hold Team API Data.

    :param self.team_id: The team's ID in the API
    :param self.team_url: URL to the team JSON API
    :param self.team_participant_url: URL to the JSON api for participants in the team.
    :param self.output_folder: The folder for the output text files
    :param currency_symbol: for formatting text
    :param self.team_info: a dictionary to values for output to text files
    :param self.participant_calculation_dict: dictionary holding output for txt files
    :param self.top_5_participant_list: a list of the top 5 team participants by amount donated.
    :param self.team_json: A dictionary to hold JSON info from the API
    :param self.team_goal: the fundraising goal of the team.
    :param self.team_captain: The name of the team captain.
    :param self.total_raised: The total amount raised by the team.
    :param self.num_donations: The total amount of donations to the team.
    :param self.top_5_participant_list: The top 5 participants in the team
    :param self.participant_list: a list of the most recent participants
    """

    def __init__(self, team_id: str, output_folder: str, currency_symbol: str):
        """Set the team variables."""
        self.team_id: str = team_id
        # urls
        team_url_base: str = f"{base_api_url}/teams/"
        self.team_url: str = f"{team_url_base}{team_id}"
        self.team_participant_url: str = f"{self.team_url}/participants"
        # misc
        self.output_folder: str = output_folder
        self.currency_symbol: str = currency_symbol
        self.team_info = {}
        self.participant_calculation_dict: dict = {}
        self.top_5_participant_list = []
        self.team_json: dict = {}
        self.team_goal: int = 0
        self.team_captain: str = ""
        self.total_raised: int = 0
        self.num_donations: int = 0
        self.top_5_participant_list: list = []
        self.participant_list: list = []

    def get_team_json(self):
        """Get team info from JSON api."""
        self.team_json = extralife_io.get_JSON(self.team_url)
        if not self.team_json:
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
        """Get team participant info from API."""
        self.participant_list = []
        team_participant_json = extralife_io.get_JSON(self.team_participant_url)
        if not team_participant_json:
            print("couldn't get to URL")
        elif len(team_participant_json) == 0:
            print("No team participants!")
        else:
            self.participant_list = [TeamParticipant(team_participant_json[participant])
                                     for participant in range(0, len(team_participant_json))]

    def get_top_5_participants(self):
        """Get team participants."""
        top5_team_participant_json = extralife_io.get_JSON(self.team_participant_url, True)
        if not top5_team_participant_json:
            print("Couldn't get top 5 team participants")
        elif len(top5_team_participant_json) == 0:
            print("No team participants!")
        else:
            self.top_5_participant_list =\
                [TeamParticipant(top5_team_participant_json[participant])
                 for participant in range(0, len(top5_team_participant_json))]

    def _top_participant(self):
        """Get Top Team Participant.

        This should just grab element 0 from self.top_5_participant_list instead of hitting API twice
        """
        if len(self.top_5_participant_list) == "0":
            print("No participants")
        else:
            return (f"{self.top_5_participant_list[0].name} - $"
                    f"{self.top_5_participant_list[0].amount:,.2f}")

    def _participant_calculations(self) -> None:
        self.participant_calculation_dict['Team_TopParticipantNameAmnt'] = self._top_participant()
        self.participant_calculation_dict['Team_Top5ParticipantsHorizontal'] = \
            extralife_io.multiple_format(self.top_5_participant_list, False, True, self.currency_symbol, 5)
        self.participant_calculation_dict['Team_Top5Participants'] = \
            extralife_io.multiple_format(self.top_5_participant_list, False, False, self.currency_symbol, 5)

    def write_text_files(self, dictionary: dict):
        """Write info to text files.

        :param dictionary: The dictionary containing the values to write out to text files.
        """
        extralife_io.write_text_files(dictionary, self.output_folder)

    def team_run(self):
        """Get team info from API."""
        self.get_team_json()
        self.write_text_files(self.team_info)

    def participant_run(self):
        """Get and calculate team participant info."""
        self.get_participants()
        self.get_top_5_participants()
        self._participant_calculations()
        self.write_text_files(self.participant_calculation_dict)

    def __str__(self):
        team_info = ""
        if self.team_json:
            team_info = f"Team goal is {self.team_info['Team_goal']}."
        if self.team_id:
            return f"A team found at {self.team_url} {team_info}."
        else:
            return "Not a valid team - no team_id."


if __name__ == "__main__":
    # debug next line
    folder = "/home/ermesa/Programming Projects/python/extralife/testOutput"
    my_team = Team("44013", folder, "$")
    my_team.get_team_json()
    my_team.get_participants()
    my_team._participant_calculations()
    my_team.write_text_files(my_team.team_info)
    my_team.write_text_files(my_team.participant_calculation_dict)
