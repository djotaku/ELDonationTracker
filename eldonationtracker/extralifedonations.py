"""Grabs donor JSON data and outputs to files."""

import time

from eldonationtracker import ipc as ipc
from eldonationtracker import donation as donation
from eldonationtracker import donor as donor
from eldonationtracker import extralife_IO as extralife_IO
from eldonationtracker import team as team


class Participant:
    """Owns all the attributes under the participant API.

    Also owns the results of any calculated data.

    Participant.conf variables:

    :param ExtraLifeID: the participant's extra life ID
    :type ExtraLifeID: int
    :param textFolder: where the output txt files will be written on disk
    :type textFolder: str
    :param CurrencySymbol: for the output txt files
    :type CurrencySymbol: str
    :param donors_to_display: for txt files that display multiple donors\
    (or donations), the number of them that should be written to the\
    text file.
    :type donors_to_display: int

    Donor Drive API api info at https://github.com/DonorDrive/PublicAPI

    Donor Drive Variables:

    :param participant_url: API info for participant
    :type participant_url: str
    :param donorURL: donation API info (should be renamed to donationURL)
    :type donorURL: str
    :param participant_donor_URL: API info for donors. Useful for calculating\
    top donor.
    :type participant_donor_URL: str
    :param participantinfo: a dictionary holding data from participantURL:

                     - totalRaised: total money raised
                     - numDonations: number of donations
                     - averageDonation: this doesn't come from the API,\
                       it's calculated in this class.
                     - goal: the participant's fundraising goal
    :type participantinfo: dict
    :param myteam: An instantiation of a team class for the participant's team.
    :type myteam: cls: eldonationtracker.team
    :param donationlist: a list of Donation class ojects made of donations to\
    this participant
    :type donationlist: list

    Helper Variables:

    :param donorcalcs: a dictionary holding values for txt ouput:

                - LastDonationNameAmnt: most recent donation,
                                        donor name, amount of donation
                - TopDonorNameAmnt: top donor name and sum of donations
                - lastNDonationNameAmts: based on value of donors_to_display
                                         above, a list of the last N donor
                                         names and donation amounts
                - lastNDonationNameAmtsMessage: same with messages
                - lastNDonationNameAmtsMessageHorizontal: same, but horizontal
                - lastNDonationNameAmtsHorizontal: same, but no message
    :type donorcalcs: dict
    :param loop: set to true on init, it's there so that the GUI can stop the\
    loop.(if the GUI is being used. Otherwise, no big deal)
    :type loop: bool
    """

    def __init__(self, participant_conf):
        """Load in config from participant.conf and creates the URLs."""
        (self.ExtraLifeID, self.textFolder,
         self.CurrencySymbol, self.TeamID,
         self.donors_to_display) = participant_conf.get_CLI_values()
        # urls
        self.participant_url = f"https://www.extra-life.org/api/participants/{self.ExtraLifeID}"
        self.donation_url = f"https://www.extra-life.org/api/participants/{self.ExtraLifeID}/donations"
        self.participant_donor_URL = f"https://www.extra-life.org/api/participants/{self.ExtraLifeID}/donors"
        # donor calculations
        self.donorcalcs = {}
        self.donorcalcs['LastDonationNameAmnt'] = "No Donors Yet"
        self.donorcalcs['TopDonorNameAmnt'] = "No Donors Yet"
        self.donorcalcs['lastNDonationNameAmts'] = "No Donors Yet"
        self.donorcalcs['lastNDonationNameAmtsMessage'] = "No Donors Yet"
        self.donorcalcs['lastNDonationNameAmtsMessageHorizontal'] = "No Donors Yet"
        self.donorcalcs['lastNDonationNameAmtsHorizontal'] = "No Donors Yet"
        self.participantinfo = {}

        # misc
        self.loop = True
        ipc.writeIPC(self.textFolder, "0")
        self.myteam = team.Team(self.TeamID,
                                self.textFolder,
                                self.CurrencySymbol)

    def _get_participant_JSON(self):
        """Get JSON data for participant information.

        Some values that I will want to track as
        numbers will go as class attributes, but all of them will
        go into the dictionary participantinfo in the way they'll
        be written to files.
        """
        participant_json = extralife_IO.get_JSON(self.participant_url)
        if participant_json == 0:
            print("Couldn't access participant JSON.")
        else:
            self.ParticipantTotalRaised = participant_json['sumDonations']
            self.ParticipantNumDonations = participant_json['numDonations']
            try:
                self.averagedonation = self.ParticipantTotalRaised/self.ParticipantNumDonations
            except ZeroDivisionError:
                self.averagedonation = 0
            self.participantgoal = participant_json['fundraisingGoal']

        # the dictionary:
        self.participantinfo['totalRaised'] = self.CurrencySymbol+'{:.2f}'.format(participant_json['sumDonations'])
        self.participantinfo["numDonations"] = str(participant_json['numDonations'])
        self.participantinfo["averageDonation"] = self.CurrencySymbol+'{:.2f}'.format(self.averagedonation)
        self.participantinfo["goal"] = self.CurrencySymbol+'{:.2f}'.format(self.participantgoal)

    def _get_donations(self):
        """Get the donations from the JSON and create the donation objects."""
        self.donationlist = []
        donation_json = extralife_IO.get_JSON(self.donation_url)
        if donation_json == 0:
            print("couldn't access donation page")
        elif len(donation_json) == 0:
            print("No donors!")
        else:
            self.donationlist = [donation.Donation(donation_json[donor].get('displayName'),
                                                   donation_json[donor].get('message'),
                                                   donation_json[donor].get('amount')) for donor in range(0, len(donation_json))]

    def _top_donor(self):
        """Return Top Donor from server.

        Uses donor drive's sorting to get the top guy or gal.
        """
        top_donor_json = extralife_IO.get_JSON(self.participant_donor_URL,
                                               True)
        if top_donor_json == 0:
            print("Couldn't access top donor data")
        else:
            top_donor = donor.Donor(top_donor_json[0])
            return extralife_IO.single_format(top_donor, False,
                                          self.CurrencySymbol)

    def _donor_calculations(self):
        self.donorcalcs['LastDonationNameAmnt'] = extralife_IO.single_format(self.donationlist[0], False, self.CurrencySymbol)
        try:
            self.donorcalcs['TopDonorNameAmnt'] = self._top_donor()
        except:
            pass
        self.donorcalcs['lastNDonationNameAmts'] = extralife_IO.multiple_format(self.donationlist, False, False, self.CurrencySymbol, int(self.donors_to_display))
        self.donorcalcs['lastNDonationNameAmtsMessage'] = extralife_IO.multiple_format(self.donationlist, True, False, self.CurrencySymbol, int(self.donors_to_display))
        self.donorcalcs['lastNDonationNameAmtsMessageHorizontal'] = extralife_IO.multiple_format(self.donationlist, True, True, self.CurrencySymbol, int(self.donors_to_display))
        self.donorcalcs['lastNDonationNameAmtsHorizontal'] = extralife_IO.multiple_format(self.donationlist, False, True, self.CurrencySymbol, int(self.donors_to_display))

    def write_text_files(self, dictionary):
        """Write OBS/XSplit display info to text files.

        It uses the helper function extralife_IO.write_text_files to\
        handle the task.

        :param dictionary: Dictionary containing values to write to text files\
        . The key will become the filename. The value will be written to the\
        file.
        :type dictionary: dict
        """
        extralife_IO.write_text_files(dictionary, self.textFolder)

    def run(self):
        """Run loop to get participant data.

        This should run getParticipantJSON, getDonors,
        the calculations methnods, and the methods to
        write to text files.

        .. warning:: This will be changed in a future version\
        to no longer be a loop and instead the loop will be in the\
        if __name__=__main__ part. This will make it more consistent with\
        the way team.py works and will enable some better efficiencies\
        with the GUI.
        """
        # by taking the while loop out of here, can make unit tests
        self._get_participant_JSON()
        number_of_dononations = self.ParticipantNumDonations
        self.write_text_files(self.participantinfo)
        self._get_donations()
        if self.donationlist:
            self._donor_calculations()
            self.write_text_files(self.donorcalcs)
        if self.TeamID:
            self.myteam.team_run()
        while self.loop:
            self._get_participant_JSON()
            self.write_text_files(self.participantinfo)
            if self.TeamID:
                self.myteam.participant_run()
            if self.ParticipantNumDonations > number_of_dononations:
                print("A new donor!")
                number_of_dononations = self.ParticipantNumDonations
                self._get_donations()
                self._donor_calculations()
                self.write_text_files(self.donorcalcs)
                ipc.writeIPC(self.textFolder, "1")
            if self.TeamID:
                self.myteam.team_run()
            print(time.strftime("%H:%M:%S"))
            time.sleep(30)

    def stop(self):
        """Stop the loop."""
        print("stopping now...")
        self.loop = False


if __name__ == "__main__":
    participant_conf = extralife_IO.ParticipantConf()
    p = Participant(participant_conf)
    p.run()
