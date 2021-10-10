"""Contains classes pertaining to teams."""
import logging
from rich import print
from rich.logging import RichHandler
from typing import Tuple, List

from donordrivepython.api.team import Team as DonorDriveTeam
import eldonationtracker.utils.extralife_io
from eldonationtracker.utils import extralife_io as extralife_io

# logging
team_log = logging.getLogger("Team:")
team_log.setLevel(logging.INFO)


class Team(DonorDriveTeam):
    """Hold Team API Data."""

    def __init__(self, team_id: str, output_folder: str, currency_symbol: str, donors_to_display: str,
                 base_api_url: str):
        DonorDriveTeam.__init__(self, team_id, output_folder, currency_symbol, donors_to_display, base_api_url)

    def write_text_files(self, dictionary: dict) -> None:  # pragma: no cover
        """Write info to text files.

        :param dictionary: The dictionary containing the values to write out to text files.
        """
        extralife_io.write_text_files(dictionary, self.output_folder)

    def team_run(self) -> None:
        """A public method to update and output team and team participant info."""
        logging.debug("I am in team_run")
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


if __name__ == "__main__":  # pragma no cover
    # debug next line
    folder = "/home/ermesa/Programming Projects/python/extralife/testOutput"
    my_team = Team("44013", folder, "$", "5")
    my_team.team_api_info()
    my_team.participant_run()
