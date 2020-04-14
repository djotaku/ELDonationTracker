"""Grabs donor JSON data and outputs to files."""

import time

from eldonationtracker import ipc as ipc
from eldonationtracker import donation as donation
from eldonationtracker import donor as donor
from eldonationtracker import extralife_io as extralife_io
from eldonationtracker import team as team
from eldonationtracker import base_api_url


class Participant:
    """Owns all the attributes under the participant API.

    Also owns the results of any calculated data.

    Participant.conf variables:

    :param self.ExtraLifeID: the participant's extra life ID
    :type ExtraLifeID: int
    :param self.textFolder: where the output txt files will be written on disk
    :type textFolder: str
    :param self.CurrencySymbol: for the output txt files
    :type CurrencySymbol: str
    :param self.donors_to_display: for txt files that display multiple donors\
    (or donations), the number of them that should be written to the\
    text file.
    :type donors_to_display: int

    Donor Drive API api info at https://github.com/DonorDrive/PublicAPI

    Donor Drive Variables:

    :param self.participant_url: API info for participant
    :type self.participant_url: str
    :param self.donorURL: donation API info (should be renamed to donationURL)
    :type self.donorURL: str
    :param self.participant_donor_URL: API info for donors. Useful for calculating\
    top donor.
    :type self.participant_donor_URL: str
    :param self.participantinfo: a dictionary holding data from participantURL:

                     - totalRaised: total money raised
                     - numDonations: number of donations
                     - averageDonation: this doesn't come from the API,\
                       it's calculated in this class.
                     - goal: the participant's fundraising goal
    :type self.participantinfo: dict
    :param self.myteam: An instantiation of a team class for the participant's team.
    :type myteam: cls: eldonationtracker.team
    :param self.donationlist: a list of Donation class ojects made of donations to\
    this participant
    :type donation_list: list

    Helper Variables:

    :param self.donation_formatted_output: a dictionary holding values for txt ouput:

                - LastDonationNameAmnt: most recent donation,
                                        donor name, amount of donation
                - TopDonorNameAmnt: top donor name and sum of donations
                - lastNDonationNameAmts: based on value of donors_to_display
                                         above, a list of the last N donor
                                         names and donation amounts
                - lastNDonationNameAmtsMessage: same with messages
                - lastNDonationNameAmtsMessageHorizontal: same, but horizontal
                - lastNDonationNameAmtsHorizontal: same, but no message
    :type donation_formatted_output: dict
    :param self.loop: set to true on init, it's there so that the GUI can stop the\
    loop.(if the GUI is being used. Otherwise, no big deal)
    :type loop: bool
    """

    def __init__(self, participant_conf):
        """Load in config from participant.conf and creates the URLs."""
        (self.ExtraLifeID, self.textFolder,
         self.CurrencySymbol, self.TeamID,
         self.donors_to_display) = participant_conf.get_CLI_values()
        # urls
        self.participant_url = f"{base_api_url}/participants/{self.ExtraLifeID}"
        self.donation_url = f"{self.participant_url}/donations"
        self.participant_donor_URL = f"{self.participant_url}/donors"

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
        self.teamName: str = ""
        self.avatar_image_url: str = ""
        self.stream_is_live: bool = False
        self.is_team_captain: bool = False
        self.sum_pledges: int = 0
        # end attributes that need to be implemented in self._get_participant_info

        self.participant_formatted_output = {'totalRaised': f"{self.CurrencySymbol}0.00",
                                             'averageDonation': f"{self.CurrencySymbol}0.00",
                                             'goal': f"{self.CurrencySymbol}0.00"}

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
        self.loop = True
        ipc.writeIPC(self.textFolder, "0")
        self.myteam = team.Team(self.TeamID,
                                self.textFolder,
                                self.CurrencySymbol)

    def _get_participant_info(self):
        """Get JSON data for participant information.

        :returns: JSON data for self.total_raised, self.number_of_donations, and self.goal.
        """
        participant_json = extralife_io.get_JSON(self.participant_url)
        if not participant_json:
            print("Couldn't access participant JSON.")
            return self.total_raised, self.number_of_donations, self.goal
        else:
            return participant_json['sumDonations'], participant_json['numDonations'],\
                   participant_json['fundraisingGoal']

    def _format_participant_info_for_output(self, participant_attribute) -> str:
        """Format participant info for output to text files.

        :param participant_attribute: the data to be formatted for the output.
        :returns: A string with the formatted information.
        """
        formatted_output = f"{self.CurrencySymbol}{participant_attribute:,.2f}"
        return formatted_output

    def _fill_participant_dictionary(self) -> None:
        """Fill up self.participant_formatted_output ."""
        self.participant_formatted_output["totalRaised"] = self._format_participant_info_for_output(self.total_raised)
        self.participant_formatted_output["averageDonation"] = self._format_participant_info_for_output(self.average_donation)
        self.participant_formatted_output["goal"] = self._format_participant_info_for_output(self.goal)

    def _calculate_average_donation(self):
        """Calculate the average donation amount.

        :returns: The average or 0.
        """
        try:
            return self.total_raised / self.number_of_donations
        except ZeroDivisionError:
            return 0

    def _get_donations(self, donations: list) -> list:
        """Get the donations from the JSON and create the donation objects.

        If the API can't be reached, the same list is returned. Only new donations are added to the list at the end.

        :param donations: A list consisting of donor.Donation objects.
        :returns: A list of donor.Donation objects.
        """
        donation_json = extralife_io.get_JSON(self.donation_url)
        if not donation_json:
            print("couldn't access donation page")
            return donations
        elif len(donation_json) == 0:
            print("No donations!")
            return donations
        else:
            donation_list = [donation.Donation(donation_json[this_donation].get('displayName'),
                                               donation_json[this_donation].get('message'),
                                               donation_json[this_donation].get('amount'),
                                               donation_json[this_donation].get('donorID'),
                                               donation_json[this_donation].get('avatarImageURL'),
                                               donation_json[this_donation].get('createdDateUTC'),
                                               donation_json[this_donation].get('donationID'))
                             for this_donation in range(0, len(donation_json))]
            if len(donations) == 0:
                return donation_list
            else:
                for a_donation in reversed(donation_list):
                    donations.insert(0, a_donation) if a_donation not in donations else donations
                return donations

    # make a top donation method, but only call it once. After that, just update it if the new donation that comes in is
    # larger

    def _get_top_donor(self):
        """Return Top Donor from server.

        Uses donor drive's sorting to get the top guy or gal.
        """
        top_donor_json = extralife_io.get_JSON(self.participant_donor_URL, True)
        if not top_donor_json:
            print("Couldn't access top donor data")
            return self.top_donor
        else:
            return donor.Donor(top_donor_json[0])

    def _format_donor_information_for_output(self) -> None:
        """Format the donor attributes for the output files."""
        self.donor_formatted_output['TopDonorNameAmnt'] = extralife_io.single_format(self.top_donor, False,
                                                                                     self.CurrencySymbol)

    def _format_donation_information_for_output(self) -> None:
        """Format the donation attributes for the output files."""
        self.donation_formatted_output['LastDonationNameAmnt'] = extralife_io.single_format(self.donation_list[0],
                                                                                            False, self.CurrencySymbol)
        self.donation_formatted_output['lastNDonationNameAmts'] = extralife_io.multiple_format(self.donation_list, False, False, self.CurrencySymbol, int(self.donors_to_display))
        self.donation_formatted_output['lastNDonationNameAmtsMessage'] = extralife_io.multiple_format(self.donation_list, True, False, self.CurrencySymbol, int(self.donors_to_display))
        self.donation_formatted_output['lastNDonationNameAmtsMessageHorizontal'] = extralife_io.multiple_format(self.donation_list, True, True, self.CurrencySymbol, int(self.donors_to_display))
        self.donation_formatted_output['lastNDonationNameAmtsHorizontal'] = extralife_io.multiple_format(self.donation_list, False, True, self.CurrencySymbol, int(self.donors_to_display))

    def write_text_files(self, dictionary: dict) -> None:
        """Write OBS/XSplit display info to text files.

        It uses the helper function extralife_IO.write_text_files to handle the task.

        :param dictionary: Dictionary containing values to write to text files\
        . The key will become the filename. The value will be written to the\
        file.
        :type dictionary: dict
        """
        extralife_io.write_text_files(dictionary, self.textFolder)

    def run(self) -> None:
        """Run loop to get participant data.

        This should run getParticipantJSON, getDonors,
        the calculations methods, and the methods to
        write to text files.

        .. warning:: This will be changed in a future version
        to no longer be a loop and instead the loop will be in the\
        if __name__=__main__ part. This will make it more consistent with\
        the way team.py works and will enable some better efficiencies\
        with the GUI.
        """
        # PARTICIPANT BLOCK ############################
        self.total_raised, self.number_of_donations, self.goal = self._get_participant_info()
        self.average_donation = self._calculate_average_donation()
        self._fill_participant_dictionary()
        self.write_text_files(self.participant_formatted_output)
        ##############################################################
        number_of_donations = self.number_of_donations
        # I think (and this may already be in issue #102, but should only get donations if self.number_of_donations is
        # greater than 0.
        # DONATION BLOCK #######################################
        self.donation_list = self._get_donations(self.donation_list)
        self._get_top_donor()
        if len(self.donation_list) > 0:
            self._format_donation_information_for_output()
            self._format_donor_information_for_output()
            self.write_text_files(self.donation_formatted_output)
        #########################################################
        # TEAM BLOCK ############################################
        if self.TeamID:
            self.myteam.team_run()
        ##########################################################
        while self.loop:
            self._get_participant_info()
            self.write_text_files(self.participant_formatted_output)
            if self.TeamID:
                self.myteam.participant_run()
            if self.number_of_donations > number_of_donations:
                print("A new donor!")
                number_of_donations = self.number_of_donations
                self.donation_list = self._get_donations(self.donation_list)
                self._get_top_donor()
                self._format_donation_information_for_output()
                self._format_donor_information_for_output()
                self.write_text_files(self.donation_formatted_output)
                ipc.writeIPC(self.textFolder, "1")
            if self.TeamID:
                self.myteam.team_run()
            print(time.strftime("%H:%M:%S"))
            time.sleep(30)

    def stop(self):
        """Stop the loop."""
        print("stopping now...")
        self.loop = False

    def __str__(self):
        return f"A participant with Extra Life ID {self.ExtraLifeID}. Team info: {self.myteam}"


if __name__ == "__main__":  # pragma: no cover
    participant_conf = extralife_io.ParticipantConf()
    p = Participant(participant_conf)
    p.run()
