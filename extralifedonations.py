import json
import urllib2
import time
import unicodedata

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

#api info at https://github.com/DonorDrive/PublicAPI
participantJSON=json.load(urllib2.urlopen(participant))
donorJSON=json.load(urllib2.urlopen(donors))


NumberofDonations = 0
NewNumberofDonations = 0

def writetofile(info,filename):
    "Handles all the file writes"
    f = open(textFolder+filename, 'w')
    f.write(info)
    f.close

#****** Participant INFO *******
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

def Participantlast5DonorNameAmtsMessage(JSON):
    last5DonorNameAmts=""
    for donor in range(0, len(JSON)):
        last5DonorNameAmts="%s%s - %s%.2f - %s\n" % (last5DonorNameAmts, JSON[donor]['displayName'], CurrencySymbol,JSON[donor]['amount'],unicodedata.normalize('NFKD',JSON[donor]['message']).encode('ascii','ignore'))
        if donor==4:
            break
        writetofile(last5DonorNameAmts,"last5DonorNameAmtsMessage.txt")
        
def  Participantlast5DonorNameAmtsMessageHorizontal(JSON):   
    # This is for a scrolling type update in OBS or XSplit
    last5DonorNameAmts=""
    for donor in range(0, len(JSON)):
        last5DonorNameAmts="%s%s - %s%.2f - %s | " % (last5DonorNameAmts, JSON[donor]['displayName'], CurrencySymbol,JSON[donor]['amount'],unicodedata.normalize('NFKD',JSON[donor]['message']).encode('ascii','ignore'))
        if donor==4:
            break
    writetofile(last5DonorNameAmts,"last5DonorNameAmtsMessageHorizontal.txt")

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
    ParticpantTotalRaised(participantJSON)
    ParticipantGoal(participantJSON)
    ParticipantLastDonorNameAmnt(donorJSON)
    ParticipantTopDonor(donorJSON)
    Participantlast5DonorNameAmts(donorJSON)
    Participantlast5DonorNameAmtsMessage(donorJSON)
    Participantlast5DonorNameAmtsMessageHorizontal(donorJSON)

def TeamLoop():
    if TeamID != None:
        teamJSON=json.load(urllib2.urlopen(team))
        TheTeamGoal(teamJSON)
        TheTeamTotalRaised(teamJSON)

def main():
    print "It's GO TIME!"
    participantJSON=json.load(urllib2.urlopen(participant))
    donorJSON=json.load(urllib2.urlopen(donors))
    print (time.strftime("%H:%M:%S"))
    ParticipantLoop()
    TeamLoop()
    NumberofDonations = CountDonors(participantJSON)
    NewNumberofDonations = NumberofDonations
    
    while True:
        print (time.strftime("%H:%M:%S"))
        participantJSON=json.load(urllib2.urlopen(participant))
        NewNumberofDonations = CountDonors(participantJSON)
        if NewNumberofDonations > NumberofDonations:
            #for debugging
            print "We got a new donor!"
            donorJSON=json.load(urllib2.urlopen(donors))
            ParticipantLoop()
            TeamLoop()
            NumberofDonations = NewNumberofDonations
        time.sleep(30)


if __name__=="__main__":
    main()
