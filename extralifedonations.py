#!/usr/bin/python3

import json
import urllib.request
import time
import unicodedata

class Donor:
    "This class exists to provide attributes for a donor based on what comes in from the JSON so that it doesn't have to be traversed each time a donor action needs to be taken"
    def __init__(self, name, message, amount):
        self.name = name
        self.message = message
        self.ammount = amount

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
        self.participantinfo = {'totalRaised':self.CurrencySymbol+'{:.2f}'.format(self.participantJSON['sumDonations']), "numDonations":str(self.participantJSON['numDonations']),"averageDonation":self.CurrencySymbol+'{:.2f}'.format(self.averagedonation), "goal":self.CurrencySymbol+'{:.2f}'.format(self.participantgoal)}
    
    
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
            self.donorlist = [Donor(self.donorJSON[donor]['displayName'],self.donorJSON[donor]['message'],self.donorJSON[donor]['amount']) for donor in range(0,len(self.donorJSON))]
    
    def _donor_formatting(self, donor, message): 
        if message:
            return f"{donor.name} - {self.CurrencySymbol}{donor.amount:.2f} - {donor.message}"
        else:
            return f"{donor.name} - {self.CurrencySymbol}{donor.amount:.2f}"
    
    def _last5donors(self,donors, message,horizontal):
        text = ""
        if message and not horizontal:
            for donor in range(0,len(donor)):
                text = text+self._donor_formatting(donor,message)+"\n"
                if donor==4:
                    break
            return text
        elif message and horizontal:
            for donor in range(0,len(donor)):
                text = text+self._donor_formatting(donor,message)+" | "
                if donor==4:
                    break
            return text
        elif not message:
            for donor in range(0,len(donor)):
                text = text+self._donor_formatting(donor,message)+" | "
                if donor==4:
                    break
            return text
    
    
    def _donor_calculations(self):
        self.donorcalcs = {}
        self.donorcalcs['LastDonorNameAmnt'] = self._donor_formatting(self.donorlist[0],False)
        ######################################################################################
        #need to implement top donor by defining __lt__ method in donor class
        ######################################################################################
        self.donorcalcs['last5DonorNameAmts'] = self._last5donors(self.donorlist,False,False)
        self.donorcalcs['last5DonorNameAmtsMessage'] = self._last5donors(self.donorlist,True,False)
        self.donorcalcs['last5DonorNameAmtsMessageHorizontal'] = self._last5donors(self.donorlist,True,True)
    
    def write_text_files(self):
        #in order to make this work best, probably need to instantiate the donor and participant dictionaries (will need to redo syntax on participant dictionary) to be able to write blanks to the text files in the loop and thus create the files even if there are no donors. For donorcalcs maybe instead of blanks, prepopulate with "No donors yet"
        pass
    
    def run(self):
        "This should run getParticipantJSON, getDonors, the calculations methnods, and the methods to write to text files"
        self.get_participant_JSON()
        NumberofDonors = self.ParticipantNumDonations
        self.get_donors()
        if self.donorlist:
            self._donor_calculations()
        while True:
            self.get_participant_JSON
            if self.ParticipantNumDonations > NumberofDonors:
                print("A new donor!")
                NumberofDonors = self.ParticipantNumDonations
                self.get_donors()
                self._donor_calculations()
            time.sleep(30)
                


########### OLD Non-Class Way ######################
#variables to change
ExtraLifeID=348774
textFolder="/home/ermesa/Dropbox/ELtracker/"
#textFolder="/home/ermesa/Streaming Overlays/donations/"
CurrencySymbol="$"
TeamID=None #change to TeamID=None if you aren't in a team

#create URLs
participant="http://www.extra-life.org/api/participants/"+str(ExtraLifeID)
donors="http://www.extra-life.org/api/participants/"+str(ExtraLifeID)+"/donations"
team="http://www.extra-life.org/api/teams/"+str(TeamID)

#api info at https://github.com/DonorDrive/PublicAPI


NumberofDonations = 0
NewNumberofDonations = 0

def writetofile(info,filename):
    "Handles all the file writes"
    f = open(textFolder+filename, 'w')
    f.write(info)
    f.close

def writetofiletuple(tuple):
    "Handles all the file writes"
    f = open(textFolder+tuple[1], 'w')
    f.write(tuple[0])
    f.close

def ParticipantTopDonor(JSON):
    TopDonorIndex=0
    TopDonorNameAmnt=""
    for donor in range(0,len(JSON)):
        #need to deal with donations where they hid the donationAmount
        if JSON[donor]['amount'] == None:
            print("skipping a null donation amount")
        elif int(JSON[donor]['amount'])>int(JSON[TopDonorIndex]['amount']):
            TopDonorIndex=donor
        TopDonorNameAmnt=str(JSON[TopDonorIndex]['displayName'])+" - "+CurrencySymbol+'{:.2f}'.format(JSON[TopDonorIndex]['amount'])
    return(TopDonorNameAmnt,"TopDonorNameAmnt.txt")


#****** Team Info *******

def TheTeamGoal(JSON):
    TeamGoal=CurrencySymbol+'{:.2f}'.format(JSON['fundraisingGoal'])
    writetofile(TeamGoal,"TeamGoal.txt")
    
def TheTeamTotalRaised(JSON):
    TeamTotalRaised=CurrencySymbol+'{:.2f}'.format(JSON['sumDonations'])
    writetofile(TeamTotalRaised,"TeamTotalRaised.txt")
    
def CountDonors(JSON):
    return int(JSON['numDonations'])


#***** LOOPS ******* 

def ParticipantLoop():
    try:
        participantJSON=json.load(urllib.request.urlopen(participant))
    except urllib.error.HTTPError:
        print("Couldn't get to participant URL. Check ExtraLifeID. Or server may be unavailable. (participant loop)")
    try:
        donorJSON=json.load(urllib.request.urlopen(donors))
    except urllib.error.HTTPError:
        print("Couldn't get to donor URL. Check ExtraLifeID. Or server may be unavailable. (participant loop)")
    writetofiletuple(ParticpantTotalRaised(participantJSON))
    writetofiletuple(ParticipantGoal(participantJSON))
    writetofiletuple(ParticipantNumDonations(participantJSON))
    writetofiletuple(ParticipantAvgDonation(participantJSON))
    writetofiletuple(ParticipantLastDonorNameAmnt(donorJSON))
    writetofiletuple(ParticipantTopDonor(donorJSON))
    writetofiletuple(Participantlast5DonorNameAmts(donorJSON))
    writetofiletuple(Participantlast5DonorNameAmtsMessage(donorJSON))
    writetofiletuple(Participantlast5DonorNameAmtsMessageHorizontal(donorJSON))

def TeamLoop():
    if TeamID != None:
        teamJSON=json.load(urllib.request.urlopen(team))
        TheTeamGoal(teamJSON)
        TheTeamTotalRaised(teamJSON)

def main():
    print ("It's GO TIME!!")
    print (time.strftime("%H:%M:%S"))
    ParticipantLoop()
    TeamLoop()
    try:
        participantJSON=json.load(urllib.request.urlopen(participant))
    except urllib.error.HTTPError:
        print("Couldn't get to participant URL. Check ExtraLifeID. Or server may be unavailable.")    
    NumberofDonations = CountDonors(participantJSON)
    NewNumberofDonations = NumberofDonations
    
    while True:
        print (time.strftime("%H:%M:%S"))
        try:
            participantJSON=json.load(urllib.request.urlopen(participant))
        except urllib.error.HTTPError:
            print("Couldn't get to participant URL. Check ExtraLifeID. Or server may be unavailable.")
        NewNumberofDonations = CountDonors(participantJSON)
        if NewNumberofDonations > NumberofDonations:
            #for debugging
            print("We got a new donor!")
            NumberofDonations = NewNumberofDonations
            ParticipantLoop()
            TeamLoop()
        time.sleep(30)


if __name__=="__main__":
#    main()
    p = Participant()
    print(p.donorURL)
    p.run()
