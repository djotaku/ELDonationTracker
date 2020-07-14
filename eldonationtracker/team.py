"""Contains classes pertaining to teams."""
from rich import print
from typing import Tuple, List

from eldonationtracker import extralife_io as extralife_io
from eldonationtracker import base_api_url
from eldonationtracker.team_participant import TeamParticipant
from eldonationtracker import donation as donation


class Team:
    """Hold Team API Data.

    :param self.team_id: The team's ID in the API
    :param self.team_url: URL to the team JSON API
    :param self.team_participant_url: URL to the JSON api for participants in the team.
    :param self.team_donation_url: URL to the JSON api for donations to the team
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

    def __init__(self, team_id: str, output_folder: str, currency_symbol: str, donors_to_display:str):
        """Set the team variables."""
        self.team_id: str = team_id
        # urls
        team_url_base: str = f"{base_api_url}/teams/"
        self.team_url: str = f"{team_url_base}{team_id}"
        self.team_participant_url: str = f"{self.team_url}/participants"
        self.team_donation_url: str = f"{self.team_url}/donations"
        # misc
        self.output_folder: str = output_folder
        self.currency_symbol: str = currency_symbol
        self.donors_to_display: str = donors_to_display
        # team info
        self.team_info: dict = {}
        self.team_json: dict = {}
        self.team_goal: int = 0
        self.team_captain: str = ""
        self.total_raised: int = 0
        self.num_donations: int = 0
        # donor info
        self.participant_calculation_dict: dict = {}
        self.top_5_participant_list: List[TeamParticipant] = []
        self.participant_list: List[TeamParticipant] = []
        # donation info
        self.donation_list: List[donation.Donation] = []
        self.donation_formatted_output: dict = {'Team_LastDonationNameAmnt': "No Donations Yet",
                                                'Team_lastNDonationNameAmts': "No Donations Yet",
                                                'Team_lastNDonationNameAmtsMessage': "No Donations Yet",
                                                'Team_lastNDonationNameAmtsMessageHorizontal': "No Donations Yet",
                                                'Team_lastNDonationNameAmtsHorizontal': "No Donations Yet"}

    def _get_team_json(self) -> Tuple[int, str, int, int]:
        """Get team info from JSON api."""
        self.team_json = extralife_io.get_json(self.team_url)
        if not self.team_json:
            print("[bold magenta]Could not get team JSON[/bold magenta]")
            return self.team_goal, self.team_captain, self.total_raised, self.num_donations
        else:
            return self.team_json["fundraisingGoal"], self.team_json["captainDisplayName"],\
                   self.team_json["sumDonations"], self.team_json["numDonations"]

    def _update_team_dictionary(self) -> None:
        self.team_info["Team_goal"] = f"{self.currency_symbol}{self.team_goal:,.2f}"
        self.team_info["Team_captain"] = f"{self.team_captain}"
        self.team_info["Team_totalRaised"] = f"{self.currency_symbol}{self.total_raised:,.2f}"
        self.team_info["Team_numDonations"] = f"{self.num_donations}"

    def _get_participants(self, top5: bool) -> List[TeamParticipant]:
        """Get team participant info from API.

        Passes the JSON to the TeamParticipant class for parsing to create a team participant.

        :param top5: If true, get the list sorted by top sum of donations.

        :returns: A list of TeamParticipant objects.
        """
        team_participant_json = extralife_io.get_json(self.team_participant_url, top5)
        if not team_participant_json:
            print("[bold magenta]Couldn't get to URL or possibly no participants.[/bold magenta]")
            if top5:
                return self.top_5_participant_list
            else:
                return self.participant_list
        else:
            return [TeamParticipant(team_participant_json[participant])
                    for participant in range(0, len(team_participant_json))]

    def _top_participant(self) -> str:
        """Get Top Team Participant.

        This should just grab element 0 from self.top_5_participant_list instead of hitting API twice

        :returns: String formatted information about the top participant.
        """
        if len(self.top_5_participant_list) == 0:
            print("[bold blue] No participants[/bold blue] ")
            return "No participants."
        else:
            return (f"{self.top_5_participant_list[0].name} - $"
                    f"{self.top_5_participant_list[0].amount:,.2f}")

    def _participant_calculations(self) -> None:
        self.participant_calculation_dict['Team_TopParticipantNameAmnt'] = self._top_participant()
        self.participant_calculation_dict['Team_Top5ParticipantsHorizontal'] = \
            extralife_io.multiple_format(self.top_5_participant_list, False, True, self.currency_symbol, 5)
        self.participant_calculation_dict['Team_Top5Participants'] = \
            extralife_io.multiple_format(self.top_5_participant_list, False, False, self.currency_symbol, 5)

    def write_text_files(self, dictionary: dict) -> None:  # pragma: no cover
        """Write info to text files.

        :param dictionary: The dictionary containing the values to write out to text files.
        """
        extralife_io.write_text_files(dictionary, self.output_folder)

    def team_run(self) -> None:
        """A public method to update and output team and team participant info."""
        number_of_donations = self.num_donations
        self.team_api_info()
        if self.num_donations > number_of_donations:
            self.participant_run()
            self.donation_run()

    def team_api_info(self) -> None:
        """Get team info from API."""
        self.team_goal, self.team_captain, self.total_raised, self.num_donations = self._get_team_json()
        self._update_team_dictionary()
        self.write_text_files(self.team_info)

    def participant_run(self) -> None:  # pragma: no cover
        """Get and calculate team participant info."""
        self.participant_list = self._get_participants(top5=False)
        self.top_5_participant_list = self._get_participants(top5=True)
        self._participant_calculations()
        self.write_text_files(self.participant_calculation_dict)

    def donation_run(self) -> None:
        """Get and calculate donation information."""
        self.donation_list = donation.get_donations(self.donation_list, self.team_donation_url)
        self.donation_formatted_output = donation.format_donation_information_for_output(self.donation_list,
                                                                                         self.currency_symbol,
                                                                                         self.donors_to_display,
                                                                                         team=True)
        self.write_text_files(self.donation_formatted_output)

    def __str__(self):
        team_info = ""
        if self.team_info:
            team_info = f"Team goal is {self.team_info['Team_goal']}."
        if self.team_id:
            return f"A team found at {self.team_url}. {team_info}"
        else:
            return "Not a valid team - no team_id."


if __name__ == "__main__":  # pragma no cover
    # debug next line
    folder = "/home/ermesa/Programming Projects/python/extralife/testOutput"
    my_team = Team("44013", folder, "$", "5")
    my_team.team_api_info()
    my_team.participant_run()
