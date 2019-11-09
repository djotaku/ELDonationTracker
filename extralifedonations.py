"""Grabs donor JSON data and outputs to files."""

import json
import urllib.request
import time

import readparticipantconf
import IPC
import team

# api info at https://github.com/DonorDrive/PublicAPI


class Donor:
    """Donor Attributes.

    Class exists to provide attributes for a donor based on what comes in from
    the JSON so that it doesn't have to be traversed each time a donor action
    needs to be taken.
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
        """Donor less than comparison.

        Returns True if this Donor has a donation
        amount less than comparision.
        """
        return self.amount < object.amount


class Participant:
    """Owns all the attributes under the participant API.

    Also owns the results of any calculated data.
    """

    def __init__(self):
        """Load in config from participant.conf and creates the URLs."""
        (self.ExtraLifeID, self.textFolder,
         self.CurrencySymbol,
         self.TeamID) = readparticipantconf.CLIvalues()
        # urls
        self.participantURL = f"http://www.extra-life.org/api/participants/{self.ExtraLifeID}"
        self.donorURL = f"http://www.extra-life.org/api/participants/{self.ExtraLifeID}/donations"
        self.participant_donor_URL = f"http://www.extra-life.org/api/participants/{self.ExtraLifeID}/donors"
        self.header = {'User-Agent': 'Extra Life Donation Tracker'}
        # donor calculations
        self.donorcalcs = {}
        self.donorcalcs['LastDonorNameAmnt'] = "No Donors Yet"
        self.donorcalcs['TopDonorNameAmnt'] = "No Donors Yet"
        self.donorcalcs['last5DonorNameAmts'] = "No Donors Yet"
        self.donorcalcs['last5DonorNameAmtsMessage'] = "No Donors Yet"
        self.donorcalcs['last5DonorNameAmtsMessageHorizontal'] = "No Donors Yet"
        self.donorcalcs['last5DonorNameAmtsHorizontal'] = "No Donors Yet"
        self.participantinfo = {}

        # misc
        self.loop = True
        IPC.writeIPC("0")
        self.myteam = team.Team(self.TeamID,
                                self.textFolder,
                                self.CurrencySymbol)

    def get_participant_JSON(self):
        """Grab participant JSON from server.

        Connects to the server and grabs the participant JSON and
        populates info.Some values that I will want to track as
        numbers will go as class attributes, but all of them will
        go into the dictionary participantinfo in the way they'll
        be written to files.
        """
        try:
            request = urllib.request.Request(url=self.participantURL,
                                             headers=self.header)
            self.participantJSON = json.load(urllib.request.urlopen(request))
        except urllib.error.HTTPError:
            print(f"""Couldn't get to {self.participantURL}.
                Check ExtraLifeID.
                Or server may be unavailable.
                If you can reach that URL from your browser
                please open an issue at:
                https://github.com/djotaku/ELDonationTracker""")

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
        """Get the donors from the JSON and creates the donor objects."""
        self.donorlist = []
        try:
            request = urllib.request.Request(url=self.donorURL,
                                             headers=self.header)
            self.donorJSON = json.load(urllib.request.urlopen(request))
        except urllib.error.HTTPError:
            print(f"""Couldn't get to {self.donorURL}.
                Check ExtraLifeID.
                Or server may be unavailable.""")
        if not self.donorJSON:
            print("No donors!")
        else:
            self.donorlist = [Donor(self.donorJSON[donor].get('displayName'), self.donorJSON[donor].get('message'), self.donorJSON[donor]['amount']) for donor in range(0, len(self.donorJSON))]

    def _donor_formatting(self, donor, message):
        if message:
            return f"{donor.name} - {self.CurrencySymbol}{donor.amount:.2f} - {donor.message}"
        else:
            return f"{donor.name} - {self.CurrencySymbol}{donor.amount:.2f}"

    def _last5donors(self, donors, message, horizontal):
        text = ""
        if horizontal:
            for donor in range(0, len(donors)):
                text = text+self._donor_formatting(donors[donor], message)+" | "
                if donor == 4:
                    break
            return text
        else:
            for donor in range(0, len(donors)):
                text = text+self._donor_formatting(donors[donor], message)+"\n"
                if donor == 4:
                    break
            return text

    def _top_donor(self):
        """Grab Top Donor from server."""
        try:
            request = urllib.request.Request(url=f"{self.participant_donor_URL}?orderBy=sumDonations%20DESC",
                                             headers=self.header)
            self.participant_donor_JSON = json.load(urllib.request.urlopen(request))
        except urllib.error.HTTPError:
            print("""Couldn't get to participant donor URL.
                Check ExtraLifeID.
                Or server may be unavailable.""")
        return f"{self.participant_donor_JSON[0]['displayName']} - {self.CurrencySymbol}{self.participant_donor_JSON[0]['sumDonations']:,.2f}"

    def _donor_calculations(self):
        self.donorcalcs['LastDonorNameAmnt'] = self._donor_formatting(self.donorlist[0], False)
        self.donorcalcs['TopDonorNameAmnt'] = self._top_donor()
        self.donorcalcs['last5DonorNameAmts'] = self._last5donors(self.donorlist, False, False)
        self.donorcalcs['last5DonorNameAmtsMessage'] = self._last5donors(self.donorlist, True, False)
        self.donorcalcs['last5DonorNameAmtsMessageHorizontal'] = self._last5donors(self.donorlist, True, True)
        self.donorcalcs['last5DonorNameAmtsHorizontal'] = self._last5donors(self.donorlist, False, True)

    def write_text_files(self, dictionary):
        """Write info to text files."""
        for filename, text in dictionary.items():
            f = open(f'{self.textFolder}/{filename}.txt', 'w', encoding='utf-8')
            f.write(text)
            f.close

    def run(self):
        """Run things.

        This should run getParticipantJSON, getDonors,
        the calculations methnods, and the methods to
        write to text files.
        """
        self.get_participant_JSON()
        NumberofDonors = self.ParticipantNumDonations
        self.write_text_files(self.participantinfo)
        self.get_donors()
        if self.donorlist:
            self._donor_calculations()
            self.write_text_files(self.donorcalcs)
        if self.TeamID:
            self.myteam.team_run()
        while self.loop:
            self.get_participant_JSON()
            self.write_text_files(self.participantinfo)
            if self.TeamID:
                self.myteam.participant_run()
            if self.ParticipantNumDonations > NumberofDonors:
                print("A new donor!")
                NumberofDonors = self.ParticipantNumDonations
                self.get_donors()
                self._donor_calculations()
                self.write_text_files(self.donorcalcs)
                IPC.writeIPC("1")
            if self.TeamID:
                self.myteam.team_run()
            print(time.strftime("%H:%M:%S"))
            time.sleep(30)

    def stop(self):
        """Stop the loop."""
        print("stopping now...")
        self.loop = False


if __name__ == "__main__":
    p = Participant()
    p.run()
