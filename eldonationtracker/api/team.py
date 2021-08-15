"""Contains classes pertaining to teams."""
import logging
from rich import print
from rich.logging import RichHandler
from typing import Tuple, List

import eldonationtracker.utils.extralife_io
from eldonationtracker.utils import extralife_io as extralife_io
from eldonationtracker import base_api_url
from eldonationtracker.api.badge import Badge  # type: ignore
from eldonationtracker.api.team_participant import TeamParticipant
from eldonationtracker.api import donation as donation

# logging
team_log = logging.getLogger("Team:")
team_log.setLevel(logging.INFO)


class Team:
    """Hold Team API Data."""

    def __init__(self, team_id: str, output_folder: str, currency_symbol: str, donors_to_display: str):
        """Set the team variables.

        :param team_id: The team's ID in the API
        :type team_id: str
        :param output_folder: The folder for the output text files
        :type output_folder: str
        :param currency_symbol: for formatting text
        :type currency_symbol: str
        :param donors_to_display: the number of donors to write out to the text files
        :type donors_to_display: str
        """
        self._team_id: str = team_id
        # urls
        self._team_url_base: str = f"{base_api_url}/teams/"
        self._team_url: str = f"{self.team_url_base}{team_id}"
        self._team_participant_url: str = f"{self.team_url}/participants"
        self._team_donation_url: str = f"{self.team_url}/donations"
        # misc
        self._output_folder: str = output_folder
        self._currency_symbol: str = currency_symbol
        self._donors_to_display: str = donors_to_display
        # team info
        self._team_info: dict = {}  # a dictionary to values for output to text files
        self._team_goal: int = 0
        self._team_captain: str = ""
        self._total_raised: int = 0
        self._num_donations: int = 0
        self._team_avatar_image: str = ''
        # donor info
        self._participant_calculation_dict: dict = {}  # dictionary holding output for txt files
        self._top_5_participant_list: List[TeamParticipant] = []  # list: top 5 team participants by amount donated.
        self._participant_list: List[TeamParticipant] = []  # A list of the most recent participants
        # donation info
        self._donation_list: List[donation.Donation] = []
        self._donation_formatted_output: dict = {'Team_LastDonationNameAmnt': "No Donations Yet",
                                                 'Team_lastNDonationNameAmts': "No Donations Yet",
                                                 'Team_lastNDonationNameAmtsMessage': "No Donations Yet",
                                                 'Team_lastNDonationNameAmtsMessageHorizontal': "No Donations Yet",
                                                 'Team_lastNDonationNameAmtsHorizontal': "No Donations Yet"}
        # other API endpoints
        self._badge_url: str = f"{self.team_url}/badges"
        self._badges: list[Badge] = []

    @property
    def team_id(self) -> str:
        """The team's ID in the API."""
        return self._team_id

    @property
    def team_url_base(self) -> str:
        """The donor drive endpoint for the teams."""
        return self._team_url_base

    @property
    def team_url(self) -> str:
        """URL to the team JSON API."""
        return self._team_url

    @property
    def team_participant_url(self) -> str:
        """URL to the JSON api for participants in the team."""
        return self._team_participant_url

    @property
    def team_donation_url(self) -> str:
        """URL to the JSON api for donations to the team."""
        return self._team_donation_url

    @property
    def output_folder(self) -> str:
        """The folder for the output text files."""
        return self._output_folder

    @property
    def currency_symbol(self) -> str:
        """The currency symbol used in the output."""
        return self._currency_symbol

    @property
    def donors_to_display(self) -> str:
        """The number of donors to write out to the output file."""
        return self._donors_to_display

    @property
    def team_goal(self) -> int:
        """The fundraising goal of the team."""
        return self._team_goal

    @property
    def team_captain(self) -> str:
        """The name of the team captain."""
        return self._team_captain

    @property
    def total_raised(self) -> int:
        """The total amount raised by the team."""
        return self._total_raised

    @property
    def num_donations(self) -> int:
        """The number of donations to the team."""
        return self._num_donations

    @property
    def team_avatar_image(self) -> str:
        """The team's avatar image."""
        if self._team_avatar_image:
            return self._team_avatar_image
        else:
            return ""

    @property
    def badge_url(self) -> str:
        """Return the team's badge URL"""
        return self._badge_url

    @property
    def badges(self) -> list[Badge]:
        """Return the list of Team's badges."""
        return self._badges

    def _get_team_json(self) -> Tuple:
        """Get team info from JSON api.

        :returns: JSON values for fundraising goal, Captain's name, total value of donations, and the # of donations.
        """
        team_json = extralife_io.get_json(self.team_url)
        if not team_json:
            team_log.warning("[bold magenta]Could not get team JSON[/bold magenta]")
            return self.team_goal, self.team_captain, self.total_raised, self.num_donations, self.team_avatar_image
        else:
            return team_json.get("fundraisingGoal"), team_json.get("captainDisplayName"), \
                   team_json.get("sumDonations"), team_json.get("numDonations"), team_json.get("avatarImageURL")

    def _update_team_dictionary(self) -> None:
        self._team_info["Team_goal"] = f"{self.currency_symbol}{self.team_goal:,.2f}"
        self._team_info["Team_captain"] = f"{self.team_captain}"
        self._team_info["Team_totalRaised"] = f"{self.currency_symbol}{self.total_raised:,.2f}"
        self._team_info["Team_numDonations"] = f"{self.num_donations}"

    def _get_participants(self, top5: bool) -> List[TeamParticipant]:
        """Get team participant info from API.

        Passes the JSON to the TeamParticipant class for parsing to create a team participant.

        :param top5: If true, get the list sorted by top sum of donations.
        :returns: A list of TeamParticipant objects.
        """
        team_participant_json = extralife_io.get_json(self.team_participant_url, top5)
        if not team_participant_json:
            team_log.warning("[bold magenta]Couldn't get to URL or possibly no participants.[/bold magenta]")
            if top5:
                return self._top_5_participant_list
            else:
                return self._participant_list
        else:
            return [TeamParticipant(participant) for participant in team_participant_json]

    def _top_participant(self) -> str:
        """Get Top Team Participant.

        This should just grab element 0 from self.top_5_participant_list instead of hitting API twice

        :returns: String formatted information about the top participant.
        """
        if len(self._top_5_participant_list) == 0:
            team_log.info("[bold blue] No participants[/bold blue] ")
            return "No participants."
        else:
            return (f"{self._top_5_participant_list[0].name} - $"
                    f"{self._top_5_participant_list[0].amount:,.2f}")

    def _participant_calculations(self) -> None:
        self._participant_calculation_dict['Team_TopParticipantNameAmnt'] = self._top_participant()
        self._participant_calculation_dict['Team_Top5ParticipantsHorizontal'] = \
            extralife_io.multiple_format(self._top_5_participant_list, False, True, self.currency_symbol, 5)
        self._participant_calculation_dict['Team_Top5Participants'] = \
            extralife_io.multiple_format(self._top_5_participant_list, False, False, self.currency_symbol, 5)

    def _update_badges(self) -> None:
        """Add all our badges to the list."""
        self._badges = extralife_io.get_badges(self.badge_url)

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
        self._team_goal, self._team_captain, self._total_raised, self._num_donations,\
            self._team_avatar_image = self._get_team_json()
        self._update_team_dictionary()
        self._update_badges()
        self.write_text_files(self._team_info)
        extralife_io.output_badge_data(self.badges, self.output_folder, team=True)

    def participant_run(self) -> None:  # pragma: no cover
        """Get and calculate team participant info."""
        self._participant_list = self._get_participants(top5=False)
        self._top_5_participant_list = self._get_participants(top5=True)
        self._participant_calculations()
        self.write_text_files(self._participant_calculation_dict)

    def donation_run(self) -> None:  # pragma: no cover
        """Get and calculate donation information."""
        self._donation_list = eldonationtracker.utils.extralife_io.get_donations(self._donation_list,
                                                                                 self.team_donation_url)
        if self._donation_list:
            self._donation_formatted_output = eldonationtracker.utils.extralife_io.format_information_for_output(
                self._donation_list, self.currency_symbol, self.donors_to_display, team=True)
            self.write_text_files(self._donation_formatted_output)
            team_avatar_for_html = "<img src=" + self.team_avatar_image + ">"
            extralife_io.write_html_files(team_avatar_for_html, 'Team_Avatar', self.output_folder)

    def __str__(self):
        team_info = ""
        if self._team_info:
            team_info = f"Team goal is {self._team_info['Team_goal']}."
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
