"""Grabs Participant JSON data and outputs to files."""

import logging
from rich import print  # type ignore
from rich.logging import RichHandler  # type ignore
import time

from donordrivepython.api import participant as donor_drive_participant  # type ignore
from donordrivepython.api.participant import Milestone as Milestone  # type ignore
from donordrivepython.api.participant import Incentive as Incentive  # type ignore
import eldonationtracker.utils.extralife_io
from eldonationtracker.api import team as team
from eldonationtracker.utils import extralife_io as extralife_io
from eldonationtracker import base_api_url

# logging
participant_log = logging.getLogger("Participant")
participant_log.setLevel(logging.INFO)


class Participant(donor_drive_participant.Participant):
    """Owns all the attributes under the participant API.

    Also owns the results of any calculated data.

    Donor Drive API api info at https://github.com/DonorDrive/PublicAPI
    """

    def __init__(self, config):
        """Load in config from participant.conf and initialize participant variables.
        """
        self.config = config
        (self._extralife_id, self._text_folder,
         self._currency_symbol, self._team_id,
         self._donors_to_display) = self.config.get_cli_values()
        donor_drive_participant.Participant.__init__(self, self._extralife_id, self._text_folder, self._currency_symbol,
                                                     self._team_id, self._donors_to_display, base_api_url)

    def set_config_values(self) -> None:
        """Set participant values, create URLs, and create Team."""
        # urls
        self._participant_url = f"{self._base_api_url}/participants/{self.donor_drive_id}"
        self._donation_url = f"{self.participant_url}/donations"
        self._participant_donor_url = f"{self.participant_url}/donors"
        self._badge_url = f"{self.participant_url}/badges"
        self._milestone_url = f"{self.participant_url}/milestones"
        self._incentive_url = f"{self.participant_url}/incentives"

        if self.team_id:
            self._my_team = team.Team(self.team_id, self.text_folder, self.currency_symbol, self.donors_to_display,
                                      self._base_api_url)


    def output_participant_data(self) -> None:  # pragma: no cover
        """Format participant data and write to text files for use by OBS or XSplit.

        A public method to do the above. Also called from the main loop.
        """
        self._fill_participant_dictionary()
        self.write_text_files(self._participant_formatted_output)
        participant_avatar_for_html = "<img src=" + self.avatar_image_url + ">"
        extralife_io.write_html_files(participant_avatar_for_html, 'Participant_Avatar', self.text_folder)

    def output_donation_data(self) -> None:
        """Write out text files for donation data.

        If there have been donations, format the data (eg horizontally, vertically, etc) and output to text files.
        If there have not yet been donations, write default data to the files.
        """
        if len(self._donation_list) > 0:
            self._format_donation_information_for_output()
            self.write_text_files(self._donation_formatted_output)
            if self._top_donation is not None:
                self.write_text_files(self._top_donation_formatted_output)
        else:
            participant_log.info("[bold blue]No donations, writing default data to files.[/bold blue]")
            self.write_text_files(self._donation_formatted_output)

    def output_donor_data(self) -> None:
        """Write out text files for donor data.

        If there have been donations, format the data (eg horizontally, vertically, etc) and output to text files.
        If there have not yet been donations, write default data to the files.
        """
        if len(self._donor_list) > 0:
            self._format_donor_information_for_output()
            self.write_text_files(self._donor_formatted_output)
            if self._top_donor is not None:
                self.write_text_files(self._top_donor_formatted_output)
        else:
            participant_log.info("[bold blue]No donors or only anonymous donors, writing default data to files.[/bold "
                                 "blue]")
            self.write_text_files(self._top_donor_formatted_output)

    def output_milestone_data(self) -> None:  # pragma: no cover
        """Write out text files for Milestone data."""
        if self.milestones:
            milestone_output = {
                f"milestone_{milestone.fundraising_goal}": f"Achievement Unlocked: {milestone.description}"
                for milestone in self.milestones
                if milestone.is_complete
            }
            self.write_text_files(milestone_output)

    def output_incentive_data(self) -> None:  # pragma: no cover
        if self.incentives:
            for incentive in self.incentives:
                incentive_dictionary = {}
                incentive_folder = f"{self.text_folder}incentives/{incentive.incentive_id}"
                incentive_dictionary["amount"] = str(incentive.amount)
                incentive_dictionary["description"] = incentive.description
                incentive_dictionary["quantity"] = str(incentive.quantity)
                incentive_dictionary["quantity_claimed"] = str(incentive.quantity_claimed)
                extralife_io.write_text_files(incentive_dictionary, incentive_folder)
                if incentive.incentive_image_url:
                    html = f"<img src='{incentive.incentive_image_url}'>"
                    extralife_io.write_html_files(html, "incentive_image", incentive_folder)

    def write_text_files(self, dictionary: dict) -> None:  # pragma: no cover
        """Write OBS/XSplit display info to text files.

        It uses the helper function extralife_IO.write_text_files to handle the task.

        :param dictionary: Dictionary containing values to write to text files\
        . The key will become the filename. The value will be written to the\
        file.
        :type dictionary: dict
        """
        extralife_io.write_text_files(dictionary, self.text_folder)

    def run(self) -> None:
        """Run to get participant, donation, donor, and team data and output to text files."""
        number_of_donations = self.number_of_donations
        self.update_participant_attributes()
        self._update_incentives()
        self.output_incentive_data()
        # Below is protection against a situation where the API is unavailable.
        # Prevents bad data being written to the participant output. Based on the assumption that it would
        # absurd to have a goal of $0.
        if self.goal != 0:
            self.output_participant_data()
            if self._first_run or self.number_of_donations > number_of_donations:  # type ignore
                if not self._first_run:  # type ignore
                    print("[bold green]A new donation![/bold green]")
                    self._new_donation = True
                self.update_donation_data()
                self.output_donation_data()
                self.update_donor_data()
                self.output_donor_data()
                self._update_badges()
                extralife_io.output_badge_data(self.badges, self.text_folder)
                self._update_milestones()
                self.output_milestone_data()
            # TEAM BLOCK ############################################
            if self.team_id:
                self.my_team.team_run()
            ##########################################################
            self._first_run = False
            participant_log.info("Finished checking API and updating text files!")
        else:
            participant_log.info("Goal was $0, most likely API unreachable. Did not update text files.")



if __name__ == "__main__":  # pragma: no cover
    participant_conf = extralife_io.ParticipantConf()
    p = Participant(participant_conf)
    while True:
        p.run()
        print(p)
        time.sleep(15)
