"""Grabs donor JSON data and outputs to files."""

import time

import IPC
import team
import extralife_IO

# api info at https://github.com/DonorDrive/PublicAPI


class Donor:
    """Donor Attributes.

    Class exists to provide attributes for a donor based on what comes in from
    the JSON so that it doesn't have to be traversed each time a donor action
    needs to be taken.
    """

    def __init__(self, json):
        """Load in values from class initialization."""
        self.json_to_attributes(json)

    def json_to_attributes(self, json):
        """Convert JSON to Donor attributes.

        May be overwritten by child classes."""
        if json.get('displayName') is not None:
            self.name = json.get('displayName')
        else:
            self.name = "Anonymous"
        self.donor_id = json.get('donorID')
        self.image_url = json.get('avatarImageURL')
        self.amount = json.get('sumDonations')
        self.number_of_dononations = json.get('numDonations')

    def __lt__(self, object):
        """Donor less than comparison.

        Returns True if this Donor has a donation
        amount less than comparision.
        """
        return self.amount < object.amount


class Donation:
    """Donation Attributes.

    Class exists to provide attributes for a donation based on what comes in
    from the JSON so that it doesn't have to be traversed each time a donor
    action needs to be taken.
    """

    def __init__(self, name, message, amount):
        """Load in values from class initialization."""
        if name is not None:
            self.name = name
        else:
            self.name = "Anonymous"
        self.message = message
        self.amount = amount

    def __lt__(self, object):
        """Donation less than comparison.

        Returns True if this donation has a donation
        amount less than comparision.
        """
        return self.amount < object.amount

class Participant:
    """Owns all the attributes under the participant API.

    Also owns the results of any calculated data.
    """

    def __init__(self, participant_conf):
        """Load in config from participant.conf and creates the URLs."""
        (self.ExtraLifeID, self.textFolder,
         self.CurrencySymbol, self.TeamID,
         self.donors_to_display) = participant_conf.get_CLI_values()
        # urls
        self.participantURL = f"https://www.extra-life.org/api/participants/{self.ExtraLifeID}"
        self.donorURL = f"https://www.extra-life.org/api/participants/{self.ExtraLifeID}/donations"
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
        IPC.writeIPC(self.textFolder, "0")
        self.myteam = team.Team(self.TeamID,
                                self.textFolder,
                                self.CurrencySymbol)

    def get_participant_JSON(self):
        """Get JSON data for participant information.

        Some values that I will want to track as
        numbers will go as class attributes, but all of them will
        go into the dictionary participantinfo in the way they'll
        be written to files.
        """
        self.participantJSON = extralife_IO.get_JSON(self.participantURL)
        self.ParticipantTotalRaised = self.participantJSON['sumDonations']
        self.ParticipantNumDonations = self.participantJSON['numDonations']
        try:
            self.averagedonation = self.ParticipantTotalRaised/self.ParticipantNumDonations
        except ZeroDivisionError:
            self.averagedonation = 0
        self.participantgoal = self.participantJSON['fundraisingGoal']

        # the dictionary:
        self.participantinfo['totalRaised'] = self.CurrencySymbol+'{:.2f}'.format(self.participantJSON['sumDonations'])
        self.participantinfo["numDonations"] = str(self.participantJSON['numDonations'])
        self.participantinfo["averageDonation"] = self.CurrencySymbol+'{:.2f}'.format(self.averagedonation)
        self.participantinfo["goal"] = self.CurrencySymbol+'{:.2f}'.format(self.participantgoal)

    def get_donors(self):
        """Get the donations from the JSON and create the donation objects."""
        self.donationlist = []
        self.donorJSON = extralife_IO.get_JSON(self.donorURL)
        if len(self.donorJSON) == 0:
            print("No donors!")
        else:
            self.donationlist = [Donation(self.donorJSON[donor].get('displayName'),
                                    self.donorJSON[donor].get('message'),
                                    self.donorJSON[donor]['amount']) for donor in range(0, len(self.donorJSON))]

    def _top_donor(self):
        """Return Top Donor from server.

        Uses donor drive's sorting to get the top guy or gal."""
        top_donor_JSON = extralife_IO.get_JSON(self.participant_donor_URL,
                                               True)
        top_donor = Donor(top_donor_JSON[0])
        return extralife_IO.single_format(top_donor, False,
                                          self.CurrencySymbol)

    def _donor_calculations(self):
        self.donorcalcs['LastDonationNameAmnt'] = extralife_IO.single_format(self.donationlist[0], False, self.CurrencySymbol)
        self.donorcalcs['TopDonorNameAmnt'] = self._top_donor()
        self.donorcalcs['lastNDonationNameAmts'] = extralife_IO.multiple_format(self.donationlist, False, False, self.CurrencySymbol, int(self.donors_to_display))
        self.donorcalcs['lastNDonationNameAmtsMessage'] = extralife_IO.multiple_format(self.donationlist, True, False, self.CurrencySymbol, int(self.donors_to_display))
        self.donorcalcs['lastNDonationNameAmtsMessageHorizontal'] = extralife_IO.multiple_format(self.donationlist, True, True, self.CurrencySymbol, int(self.donors_to_display))
        self.donorcalcs['lastNDonationNameAmtsHorizontal'] = extralife_IO.multiple_format(self.donationlist, False, True, self.CurrencySymbol, int(self.donors_to_display))

    def write_text_files(self, dictionary):
        """Write info to text files."""
        extralife_IO.write_text_files(dictionary, self.textFolder)

    def run(self):
        """Run things.

        This should run getParticipantJSON, getDonors,
        the calculations methnods, and the methods to
        write to text files.
        """
        self.get_participant_JSON()
        number_of_dononations = self.ParticipantNumDonations
        self.write_text_files(self.participantinfo)
        self.get_donors()
        if self.donationlist:
            self._donor_calculations()
            self.write_text_files(self.donorcalcs)
        if self.TeamID:
            self.myteam.team_run()
        while self.loop:
            self.get_participant_JSON()
            self.write_text_files(self.participantinfo)
            if self.TeamID:
                self.myteam.participant_run()
            if self.ParticipantNumDonations > number_of_dononations:
                print("A new donor!")
                number_of_dononations = self.ParticipantNumDonations
                self.get_donors()
                self._donor_calculations()
                self.write_text_files(self.donorcalcs)
                IPC.writeIPC(self.textFolder, "1")
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
