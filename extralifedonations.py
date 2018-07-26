import json
import urllib2
import time

#variables to change
ExtraLifeID=297674
textFolder="/home/ermesa/Dropbox/ELtracker/"
#textFolder="/home/ermesa/Streaming Overlays/donations/"
CurrencySymbol="$"
TeamID=None #change to TeamID=None if you aren't in a team

#create URLs
participant="http://www.extra-life.org/api/participants/"+str(ExtraLifeID)
donors="http://www.extra-life.org/api/participants/"+str(ExtraLifeID)+"/donations"
team="http://www.extra-life.org/api/teams/"+str(TeamID)
#I'll get back to this one
#teamroster="http://www.extra-life.org/index.cfm?fuseaction=donorDrive.teamParticipants&teamID="+str(TeamID)+"&format=json"

#api info at https://github.com/DonorDrive/PublicAPI

def writetofile(info,filename):
    "Handles all the file writes"
    f = open(textFolder+filename, 'w')
    f.write(info)
    f.close


def ParticpantTotalRaised(JSON):
    totalRaised=CurrencySymbol+'{:.2f}'.format(JSON['sumDonations'])
    writetofile(totalRaised,"totalRaised.txt")

def ParticipantGoal(JSON):
    goal=CurrencySymbol+'{:.2f}'.format(JSON['fundraisingGoal'])
    writetofile(goal,"goal.txt")
    
def ParticipantLastDonorNameAmnt(JSON):
    LastDonorNameAmnt=str(JSON[0]['displayName'])+" - "+CurrencySymbol+'{:.2f}'.format(JSON[0]['amount'])
    writetofile(LastDonorNameAmnt,"LastDonorNameAmnt.txt")

def ParticipantTopDonor(JSON):
    TopDonorIndex=0
    TopDonorNameAmnt=""
    for donor in range(0,len(JSON)):
        #need to deal with donations where they hid the donationAmount
        if JSON[donor]['amount'] == None:
            print "skipping a null donation amount"
        elif int(JSON[donor]['amount'])>int(JSON[TopDonorIndex]['amount']):
            TopDonorIndex=donor
        TopDonorNameAmnt=str(JSON[TopDonorIndex]['displayName'])+" - "+CurrencySymbol+'{:.2f}'.format(JSON[TopDonorIndex]['amount'])
    writetofile(TopDonorNameAmnt,"TopDonorNameAmnt.txt")

def Participantlast5DonorNameAmts(JSON):
    last5DonorNameAmts=""
    for donor in range(0, len(JSON)):
        last5DonorNameAmts=last5DonorNameAmts+str(JSON[donor]['displayName'])+" - "+CurrencySymbol+str(JSON[donor]['amount'])+"0\n"
        if donor==4:
            break
    writetofile(last5DonorNameAmts,"last5DonorNameAmts.txt")

def TheTeamGoal(JSON):
    TeamGoal=CurrencySymbol+'{:.2f}'.format(JSON['fundraisingGoal'])
    writetofile(TeamGoal,"TeamGoal.txt")
    
def TheTeamTotalRaised(JSON):
    TeamTotalRaised=CurrencySymbol+'{:.2f}'.format(JSON['sumDonations'])
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
        
        time.sleep(30)
