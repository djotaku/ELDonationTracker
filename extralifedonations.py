import json
import urllib2
import time

#variables to change
ExtraLifeID=196184
textFolder="/home/ermesa/Streaming Overlays/donations/"
CurrencySymbol="$"
TeamID=27284 #change to TeamID=None if you aren't in a team

#create URLs
participant="http://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID="+str(ExtraLifeID)+"&format=json"
donors="http://www.extra-life.org/index.cfm?fuseaction=donorDrive.participantDonations&participantID="+str(ExtraLifeID)+"&format=json"
team="http://www.extra-life.org/index.cfm?fuseaction=donorDrive.team&teamID="+str(TeamID)+"&format=json"
teamroster="http://www.extra-life.org/index.cfm?fuseaction=donorDrive.teamParticipants&teamID="+str(TeamID)+"&format=json"

def writetofile(info,filename):
    "Handles all the file writes"
    f = open(textFolder+filename, 'w')
    f.write(info)
    f.close


def ParticpantTotalRaised(JSON):
    totalRaised=CurrencySymbol+'{:.2f}'.format(JSON['totalRaisedAmount'])
    writetofile(totalRaised,"totalRaised.txt")

def ParticipantGoal(JSON):
    goal=CurrencySymbol+'{:.2f}'.format(JSON['fundraisingGoal'])
    writetofile(goal,"goal.txt")
    
def ParticipantLastDonorNameAmnt(JSON):
    LastDonorNameAmnt=str(JSON[0]['donorName'])+" - "+CurrencySymbol+'{:.2f}'.format(JSON[0]['donationAmount'])
    writetofile(LastDonorNameAmnt,"LastDonorNameAmnt.txt")

def ParticipantTopDonor(JSON):
    TopDonorIndex=0
    TopDonorNameAmnt=""
    for donor in range(0,len(JSON)):
        #need to deal with donations where they hid the donationAmount
        if JSON[donor]['donationAmount'] == None:
            print "skipping a null donation amount"
        elif int(JSON[donor]['donationAmount'])>int(JSON[TopDonorIndex]['donationAmount']):
            TopDonorIndex=donor
        TopDonorNameAmnt=str(JSON[TopDonorIndex]['donorName'])+" - "+CurrencySymbol+'{:.2f}'.format(JSON[TopDonorIndex]['donationAmount'])
    writetofile(TopDonorNameAmnt,"TopDonorNameAmnt.txt")

def Participantlast5DonorNameAmts(JSON):
    last5DonorNameAmts=""
    for donor in range(0, len(JSON)):
        last5DonorNameAmts=last5DonorNameAmts+str(JSON[donor]['donorName'])+" - "+CurrencySymbol+str(JSON[donor]['donationAmount'])+"0\n"
        if donor==4:
            break
    writetofile(last5DonorNameAmts,"last5DonorNameAmts.txt")

def TheTeamGoal(JSON):
    TeamGoal=CurrencySymbol+'{:.2f}'.format(JSON['fundraisingGoal'])
    writetofile(TeamGoal,"TeamGoal.txt")
    
def TheTeamTotalRaised(JSON):
    TeamTotalRaised=CurrencySymbol+'{:.2f}'.format(JSON['totalRaisedAmount'])
    writetofile(TeamTotalRaised,"TeamTotalRaised.txt")
#this part needs to be in a loop

if __name__=="__main__":
    print "It's GO TIME!"
    while True:
        
        #participant stuff
        participantJSON=json.load(urllib2.urlopen(participant))
        donorJSON=json.load(urllib2.urlopen(donors))

        print (time.strftime("%H:%M:%S"))
        
        ParticpantTotalRaised(participantJSON)
        ParticipantGoal(participantJSON)
        ParticipantLastDonorNameAmnt(donorJSON)
        ParticipantTopDonor(donorJSON)
        Participantlast5DonorNameAmts(donorJSON)
        
        if TeamID != None:
            teamJSON=json.load(urllib2.urlopen(team))
            teamrosterJSON=json.load(urllib2.urlopen(teamroster))
            TheTeamGoal(teamJSON)
            TheTeamTotalRaised(teamJSON)
        
        time.sleep(120)
