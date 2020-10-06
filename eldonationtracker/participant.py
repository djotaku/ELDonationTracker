"""Grabs Participant JSON data and outputs to files."""

from rich import print  # type ignore

import time

from eldonationtracker import donation as donation
from eldonationtracker import donor as donor
from eldonationtracker import extralife_io as extralife_io
from eldonationtracker import team as team
from eldonationtracker import base_api_url


class Participant:
    """Owns all the attributes under the participant API.

    Also owns the results of any calculated data.

    Donor Drive API api info at https://github.com/DonorDrive/PublicAPI

    :param self.extralife_id: the participant's extra life ID
    :type self.extralife_id: int
    :param self.text_folder: where the output text files will be written on disk
    :type self.text_folder: str
    :param self.currency_symbol: for the output text files
    :type self.currency_symbol: str
    :param self.donors_to_display: for text files that display multiple donors (or donations), the number of them that\
     should be written to the text file.
    :type self.donors_to_display: int
    :param self.participant_url: API info for participant
    :type self.participant_url: str
    :param self.donation_url: donation API info
    :type self.donation_url: str
    :param self.participant_donor_url: API info for donors. Useful for calculating top donor.
    :type self.participant_donor_url: str
    :param self.total_raised: total amount raised by the participant
    :type self.total_raised: int
    :param self.number_of_donations: the number of donations received by the participant
    :type self.number_of_donations: int
    :param self.average_donation: The average amount of donations for this participant
    :type self.average_donation: int
    :param self.goal: The goal for the amount of the money the participant wishes to raise
    :type self.goal: int
    :param self.participant_formatted_output: a dictionary holding data about the participant
    :type self.participant_formatted_output: dict
    :param self.my_team: An instantiation of a team class for the participant's team.
    :type self.my_team: cls: eldonationtracker.team
    :param self.donation_list: a list of Donation class objects made of donations to this participant
    :type self.donation_list: list
    :param self.donation_formatted_output: a dictionary holding values for txt output
    :type self.donation_formatted_output: dict
    """

    def __init__(self, config):
        """Load in config from participant.conf and initialize participant variables.
        """
        self.config = config
        self.extralife_id: str = ""
        self.text_folder: str = ""
        self.currency_symbol: str = ""
        self.team_id: str = ""
        self.donors_to_display: str = ""
        self.participant_url: str = ""
        self.donation_url: str = ""
        self.participant_donor_url: str = ""
        self.my_team: team.Team = None
        self.set_config_values()

        # Participant Information
        self.total_raised: int = 0
        self.number_of_donations: int = 0
        self.average_donation: int = 0
        self.goal: int = 0
        # the following need to be implemented in self._get_participant_info:
        self.event_name: str = ""
        self.donation_link_url: str = ""
        self.stream_url: str = ""
        self.extra_life_page_url: str = ""
        self.created_date_utc: str = ""
        self.team_name: str = ""
        self.avatar_image_url: str = ""
        self.stream_is_live: bool = False
        self.is_team_captain: bool = False
        self.sum_pledges: int = 0
        # end attributes that need to be implemented in self._get_participant_info

        self.participant_formatted_output = {'totalRaised': f"{self.currency_symbol}0.00",
                                             'averageDonation': f"{self.currency_symbol}0.00",
                                             'goal': f"{self.currency_symbol}0.00"}

        # donation information
        self.donation_list: list = []
        self.donation_formatted_output: dict = {'LastDonationNameAmnt': "No Donations Yet",
                                                'lastNDonationNameAmts': "No Donations Yet",
                                                'lastNDonationNameAmtsMessage': "No Donations Yet",
                                                'lastNDonationNameAmtsMessageHorizontal': "No Donations Yet",
                                                'lastNDonationNameAmtsHorizontal': "No Donations Yet"}
        # donor information
        self.top_donor = None
        self.donor_formatted_output: dict = {'TopDonorNameAmnt': "No Donors Yet"}

        # misc
        self.first_run: bool = True
        self.new_donation: bool = False

    def set_config_values(self) -> None:
        """Set participant values, create URLs, and create Team."""
        (self.extralife_id, self.text_folder,
         self.currency_symbol, self.team_id,
         self.donors_to_display) = self.config.get_cli_values()
        # urls
        self.participant_url = f"{base_api_url}/participants/{self.extralife_id}"
        self.donation_url = f"{self.participant_url}/donations"
        self.participant_donor_url = f"{self.participant_url}/donors"

        if self.team_id:
            self.my_team = team.Team(self.team_id, self.text_folder, self.currency_symbol, self.donors_to_display)

    def _get_participant_info(self):
        """Get JSON data for participant information.

        :returns: JSON data for self.total_raised, self.number_of_donations, and self.goal.
        """
        participant_json = extralife_io.get_json(self.participant_url)
        if not participant_json:
            print("[bold red]Couldn't access participant JSON.[/bold red]")
            return self.total_raised, self.number_of_donations, self.goal
        else:
            return participant_json['sumDonations'], participant_json['numDonations'],\
                   participant_json['fundraisingGoal']

    def _format_participant_info_for_output(self, participant_attribute) -> str:
        """Format participant info for output to text files.

        :param participant_attribute: the data to be formatted for the output.
        :returns: A string with the formatted information.
        """
        formatted_output = f"{self.currency_symbol}{participant_attribute:,.2f}"
        return formatted_output

    def _fill_participant_dictionary(self) -> None:
        """Fill up self.participant_formatted_output ."""
        self.participant_formatted_output["totalRaised"] =\
            self._format_participant_info_for_output(self.total_raised)
        self.participant_formatted_output["averageDonation"] =\
            self._format_participant_info_for_output(self.average_donation)
        self.participant_formatted_output["goal"] = self._format_participant_info_for_output(self.goal)
        self.participant_formatted_output["numDonations"] = str(self.number_of_donations)

    def _calculate_average_donation(self):
        """Calculate the average donation amount.

        :returns: The average or 0.
        """
        try:
            return self.total_raised / self.number_of_donations
        except ZeroDivisionError:
            return 0

    # make a top donation method, but only call it once. After that, just update it if the new donation that comes in is
    # larger

    def _get_top_donor(self):
        """Return Top Donor from server.

        Uses donor drive's sorting to get the top guy or gal.
        """
        top_donor_json = extralife_io.get_json(self.participant_donor_url, True)
        if not top_donor_json:
            print("[bold red] Couldn't access top donor data[/bold red]")
            return self.top_donor
        else:
            return donor.Donor(top_donor_json[0])

    def _format_donor_information_for_output(self) -> None:
        """Format the donor attributes for the output files."""
        self.donor_formatted_output['TopDonorNameAmnt'] = extralife_io.single_format(self.top_donor, False,
                                                                                     self.currency_symbol)

    def _format_donation_information_for_output(self) -> None:
        """Format the donation attributes for the output files."""
        self.donation_formatted_output = donation.format_donation_information_for_output(self.donation_list,
                                                                                         self.currency_symbol,
                                                                                         self.donors_to_display,
                                                                                         team=False)

    def update_participant_attributes(self) -> None:  # pragma: no cover
        """Update participant attributes.

         A public method that will update the Participant object with data from self.participant_url.

         Also called from the main loop.
         """
        self.total_raised, self.number_of_donations, self.goal = self._get_participant_info()
        self.average_donation = self._calculate_average_donation()

    def output_participant_data(self) -> None:  # pragma: no cover
        """Format participant data and write to text files for use by OBS or XSplit.

        A public method to do the above. Also called from the main loop.
        """
        self._fill_participant_dictionary()
        self.write_text_files(self.participant_formatted_output)

    def update_donation_data(self) -> None:
        """Update donation data.

        As of 5.0 it just updates the list of donations. There may be more donation-related updating in future versions.
        """
        if self.number_of_donations > 0:
            self.donation_list = donation.get_donations(self.donation_list, self.donation_url)

    def update_donor_data(self) -> None:
        """Update donor data.

        As of 5.0 it only grabs the top donor. There may be more donor-related updates in the future.
        """
        if self.number_of_donations > 0:
            self.top_donor = self._get_top_donor()

    def output_donation_data(self) -> None:
        """Write out text files for donation data.

        If there have been donations, format the data (eg horizontally, vertically, etc) and output to text files.
        If there have not yet been donations, write default data to the files.
        """
        if len(self.donation_list) > 0:
            self._format_donation_information_for_output()
            self.write_text_files(self.donation_formatted_output)
        else:
            print("[bold blue]No donations, writing default data to files.[/bold blue]")
            self.write_text_files(self.donation_formatted_output)

    def output_donor_data(self) -> None:
        """Write out text files for donor data.

        If there have been donations, format the data (eg horizontally, vertically, etc) and output to text files.
        If there have not yet been donations, write default data to the files.
        """
        if len(self.donation_list) > 0 and self.top_donor is not None:
            self._format_donor_information_for_output()
            self.write_text_files(self.donor_formatted_output)
        else:
            print("[bold blue]No donors or only anonymous donors, writing default data to files.[/bold blue]")
            self.write_text_files(self.donor_formatted_output)

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
        self.output_participant_data()
        if self.first_run or self.number_of_donations > number_of_donations:
            if not self.first_run:
                print("[bold green]A new donation![/bold green]")
                self.new_donation = True
            self.update_donation_data()
            self.output_donation_data()
            self.update_donor_data()
            self.output_donor_data()
        # TEAM BLOCK ############################################
        if self.team_id:
            self.my_team.team_run()
        ##########################################################
        self.first_run = False
        print(time.strftime("%H:%M:%S"))

    def __str__(self):
        if self.my_team:
            return f"A participant with Extra Life ID {self.extralife_id}. Team info: {self.my_team}"
        else:
            return f"A participant with Extra Life ID {self.extralife_id}."


if __name__ == "__main__":  # pragma: no cover
    participant_conf = extralife_io.ParticipantConf()
    p = Participant(participant_conf)
    while True:
        p.run()
        time.sleep(15)
