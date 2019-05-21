#!/usr/bin/python3

import json
import urllib.request
import time
import unicodedata

#api info at https://github.com/DonorDrive/PublicAPI

class Donor:
    "This class exists to provide attributes for a donor based on what comes in from the JSON so that it doesn't have to be traversed each time a donor action needs to be taken"
    def __init__(self, name, message, amount):
        self.name = name
        self.message = message
        self.amount = amount
        
    def __lt__(self,object):
        return self.amount < object.amount

class Participant:
    "Participant is a class that owns all the attributes under the participant API point; Also owns the results of any calculated data."
    
    def __init__(self):
        "Loads in config from participant.conf and creates the URLs."
        with open('participant.conf') as file:
            self.participantconf = json.load(file)
        (self.ExtraLifeID,self.textFolder,self.CurrencySymbol, self.TeamID) = (self.participantconf['ExtraLifeID'],self.participantconf['textFolder'], self.participantconf['CurrencySymbol'], self.participantconf['TeamID'])
        self.participantURL = f"http://www.extra-life.org/api/participants/{self.ExtraLifeID}"
        self.donorURL = f"http://www.extra-life.org/api/participants/{self.ExtraLifeID}/donations"
        #if need to test with donations until write unit tests: 
        #self.donorURL = f"http://www.extra-life.org/api/participants/297674/donations"
        self.teamURL = f"http://www.extra-life.org/api/teams/{self.TeamID}"
        self.donorcalcs = {}
        self.donorcalcs['LastDonorNameAmnt'] = "No Donors Yet"
        self.donorcalcs['TopDonorNameAmnt'] = "No Donors Yet"
        self.donorcalcs['last5DonorNameAmts'] = "No Donors Yet"
        self.donorcalcs['last5DonorNameAmtsMessage'] = "No Donors Yet"
        self.donorcalcs['last5DonorNameAmtsMessageHorizontal'] = "No Donors Yet"
        self.participantinfo = {}
    
    def get_participant_JSON(self):
        """Connects to the server and grabs the participant JSON and populates info.
        
        Some values that I will want to track as numbers will go as class attributes, but all of them will go into the dictionary participantinfo in the way they'll be written to files."""
        try:
            self.participantJSON=json.load(urllib.request.urlopen(self.participantURL))
        except urllib.error.HTTPError:
            print("Couldn't get to participant URL. Check ExtraLifeID. Or server may be unavailable.")
            
        self.ParticipantTotalRaised = self.participantJSON['sumDonations']
        self.ParticipantNumDonations = self.participantJSON['numDonations']
        try:
            self.averagedonation = self.ParticipantTotalRaised/self.ParticipantNumDonations
        except ZeroDivisionError:
            self.averagedonation = 0
        self.participantgoal = self.participantJSON['fundraisingGoal']
        
        #the dictionary:
        self.participantinfo['totalRaised'] =self.CurrencySymbol+'{:.2f}'.format(self.participantJSON['sumDonations'])
        self.participantinfo["numDonations"] = str(self.participantJSON['numDonations'])
        self.participantinfo["averageDonation"] = self.CurrencySymbol+'{:.2f}'.format(self.averagedonation)
        self.participantinfo["goal"] = self.CurrencySymbol+'{:.2f}'.format(self.participantgoal)
    
    
    def get_donors(self):
        "Gets the donors from the JSON and creates the donor objects."
        self.donorlist = []
        try:
            self.donorJSON=json.load(urllib.request.urlopen(self.donorURL))
        except urllib.error.HTTPError:
            print("Couldn't get to donor URL. Check ExtraLifeID. Or server may be unavailable.")
        if not self.donorJSON:
            print("No donors!")
        else:
            self.donorlist = [Donor(self.donorJSON[donor]['displayName'],self.donorJSON[donor].get('message'),self.donorJSON[donor]['amount']) for donor in range(0,len(self.donorJSON))]
    
    def _donor_formatting(self, donor, message): 
        if message:
            return f"{donor.name} - {self.CurrencySymbol}{donor.amount:.2f} - {donor.message}"
        else:
            return f"{donor.name} - {self.CurrencySymbol}{donor.amount:.2f}"
    
    def _last5donors(self,donors,message,horizontal):
        text = ""
        if message and not horizontal:
            for donor in range(0,len(donors)):
                text = text+self._donor_formatting(donors[donor],message)+"\n"
                if donor==4:
                    break
            return text
        elif message and horizontal:
            for donor in range(0,len(donors)):
                text = text+self._donor_formatting(donors[donor],message)+" | "
                if donor==4:
                    break
            return text
        elif not message:
            for donor in range(0,len(donors)):
                text = text+self._donor_formatting(donors[donor],message)+"\n"
                if donor==4:
                    break
            return text
    
    
    def _donor_calculations(self):
        self.donorcalcs['LastDonorNameAmnt'] = self._donor_formatting(self.donorlist[0],False)
        self.donorcalcs['TopDonorNameAmnt'] = self._donor_formatting(sorted(self.donorlist,reverse=True)[0],False)
        self.donorcalcs['last5DonorNameAmts'] = self._last5donors(self.donorlist,False,False)
        self.donorcalcs['last5DonorNameAmtsMessage'] = self._last5donors(self.donorlist,True,False)
        self.donorcalcs['last5DonorNameAmtsMessageHorizontal'] = self._last5donors(self.donorlist,True,True)
    
    def write_text_files(self,dictionary):
        """description"""
        for filename, text in dictionary.items():
            f = open(self.textFolder+filename+".txt", 'w')
            f.write(text)
            f.close
    
    def run(self):
        "This should run getParticipantJSON, getDonors, the calculations methnods, and the methods to write to text files"
        self.get_participant_JSON()
        NumberofDonors = self.ParticipantNumDonations
        self.write_text_files(self.participantinfo)
        self.get_donors()
        if self.donorlist:
            self._donor_calculations()
            self.write_text_files(self.donorcalcs)
        while True:
            self.get_participant_JSON()
            self.write_text_files(self.participantinfo)
            if self.ParticipantNumDonations > NumberofDonors:
                print("A new donor!")
                NumberofDonors = self.ParticipantNumDonations
                self.get_donors()
                self._donor_calculations()
                self.write_text_files(self.donorcalcs)
            print (time.strftime("%H:%M:%S"))
            time.sleep(30)
                


########### OLD Non-Class Way ######################
TeamID=None #change to TeamID=None if you aren't in a team

#create URLs
team="http://www.extra-life.org/api/teams/"+str(TeamID)


def writetofiletuple(tuple):
    "Handles all the file writes"
    f = open(textFolder+tuple[1], 'w')
    f.write(tuple[0])
    f.close

#****** Team Info *******

def TheTeamGoal(JSON):
    TeamGoal=CurrencySymbol+'{:.2f}'.format(JSON['fundraisingGoal'])
    writetofile(TeamGoal,"TeamGoal.txt")
    
def TheTeamTotalRaised(JSON):
    TeamTotalRaised=CurrencySymbol+'{:.2f}'.format(JSON['sumDonations'])
    writetofile(TeamTotalRaised,"TeamTotalRaised.txt")
    
#***** LOOPS ******* 

def TeamLoop():
    if TeamID != None:
        teamJSON=json.load(urllib.request.urlopen(team))
        TheTeamGoal(teamJSON)
        TheTeamTotalRaised(teamJSON)

########### OLD Non-Class Way ######################

if __name__=="__main__":
#    main()
    p = Participant()
    p.run()
