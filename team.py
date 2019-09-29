""" Contains classes pertaining to teams."""

import json
import urllib.request

class Team:
    """Hold Team Data."""
    def __init__(self, team_ID, folder):
        self.team_url = f"http://www.extra-life.org/api/teams/{team_ID}"
        self.team_participant_url = f"https://extra-life.org/api/teams/{team_ID}/participants"
        self.output_folder = folder
        self.team_info = {}
        self.participant_calculation_dict = {}

    def get_team_json(self):
        """Get team info from JSON api."""
        try:
            self.team_json = json.load(urllib.request.urlopen(self.team_url))
        except urllib.error.HTTPError:
            print("Couldn't get to team URL. Check team ID. Or server may be unavailable.")
        self.team_goal = self.team_json["fundraisingGoal"]
        self.team_captain = self.team_json["captainDisplayName"]
        self.total_raised = self.team_json["sumDonations"]
        self.num_donations = self.team_json["numDonations"]
        # dictionary
        self.team_info["Team_goal"] = f"{self.team_goal:,.2f}"
        self.team_info["Team_captain"] = f"{self.team_captain}"
        self.team_info["Team_totalRaised"] = f"{self.total_raised:,.2f}"
        self.team_info["Team_numDonations"] = f"{self.num_donations}"
        # debug - print statement below
        print(self.team_info)
    def get_participants(self):
        """Get team participants."""
        self.participant_list = []
        try:
            self.team_participant_json = json.load(urllib.request.urlopen(self.team_participant_url))
        except urllib.error.HTTPError:
            print("Couldn't get to team participant URL.")
        if not self.team_participant_json:
            print("No team participants!")
        else:
            self.participant_list = [TeamParticipant(self.team_participant_json[participant]['displayName'], float(self.team_participant_json[participant]['sumDonations'])) for participant in range(0, len(self.team_participant_json))]
    def _participant_calculations(self):
        self.participant_calculation_dict['Team_TopParticipantNameAmnt'] = f"{sorted(self.participant_list, reverse=True)[0].name} - ${sorted(self.participant_list, reverse=True)[0].donation_totals:,.2f}"
        # debug next line
        print(self.participant_calculation_dict['Team_TopParticipantNameAmnt'])
    def write_text_files(self, dictionary):
        """Write info to text files."""
        for filename, text in dictionary.items():
            f = open(f'{self.output_folder}/{filename}.txt', 'w')
            f.write(text)
            f.close

class TeamParticipant:
    """Participant Attributes."""
    def __init__(self, name, donation_totals):
        self.name = name
        self.donation_totals = donation_totals
    def __lt__(self, object):
        """Participant less-than comparison"""
        return self.donation_totals < object.donation_totals

if __name__ == "__main__":
    # debug next line
    folder = "/home/ermesa/programming/donationtxt/"
    myteam = Team(44013, folder)
    myteam.get_team_json()
    myteam.get_participants()
    myteam._participant_calculations()
    myteam.write_text_files(myteam.team_info)
    myteam.write_text_files(myteam.participant_calculation_dict)
