import json
import urllib2
import time

#variables to change
ExtraLifeID=196184
textFolder="/home/ermesa/Streaming Overlays/donations/"
CurrencySymbol="$"
TeamID=27284

#create URLs
participant="http://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID="+str(ExtraLifeID)+"&format=json"
donors="http://www.extra-life.org/index.cfm?fuseaction=donorDrive.participantDonations&participantID="+str(ExtraLifeID)+"&format=json"
team="http://http://www.extra-life.org/index.cfm?fuseaction=donorDrive.team&teamID="+str(TeamID)+"&format=json"
teamroster="http://www.extra-life.org/index.cfm?fuseaction=donorDrive.teamParticipants"+str(TeamID)+"&format=json"

#this part needs to be in a loop
while True:
    #Get the Info
    participantJSON=json.load(urllib2.urlopen(participant))
    donorJSON=json.load(urllib2.urlopen(donors))

    #fordebug
    #print str(participantJSON)+"\n\n"
    #print str(donorJSON)+"\n\n"
    print (time.strftime("%H:%M:%S"))

    totalRaised=CurrencySymbol+str(participantJSON['totalRaisedAmount'])
    f = open(textFolder+'totalRaised.txt', 'w')
    f.write(totalRaised)
    f.close

    goal=CurrencySymbol+str(participantJSON['fundraisingGoal'])
    f = open(textFolder+'goal.txt', 'w')
    f.write(goal)
    f.close

    LastDonorNameAmnt=str(donorJSON[0]['donorName'])+" - "+CurrencySymbol+str(donorJSON[0]['donationAmount'])
    f = open(textFolder+'LastDonorNameAmnt.txt', 'w')
    f.write(LastDonorNameAmnt)
    f.close

    #for finding top donor
    TopDonorIndex=0
    TopDonorNameAmnt=""
    for donor in range(0,len(donorJSON)):
        #need to deal with donations where they hid the donationAmount
        if donorJSON[donor]['donationAmount'] == None:
            print "skipping a null donation amount"
        elif int(donorJSON[donor]['donationAmount'])>int(donorJSON[TopDonorIndex]['donationAmount']):
            TopDonorIndex=donor
        TopDonorNameAmnt=str(donorJSON[TopDonorIndex]['donorName'])+" - "+CurrencySymbol+str(donorJSON[TopDonorIndex]['donationAmount'])
    f = open(textFolder+'TopDonorNameAmnt.txt', 'w')
    f.write(TopDonorNameAmnt)
    f.close


    last5DonorNameAmts=""
    for donor in range(0, len(donorJSON)):
        last5DonorNameAmts=last5DonorNameAmts+str(donorJSON[donor]['donorName'])+" - "+CurrencySymbol+str(donorJSON[donor]['donationAmount'])+"\n"
        if donor==4:
            break
    f = open(textFolder+'last5DonorNameAmts.txt', 'w')
    f.write(last5DonorNameAmts)
    f.close
    
    time.sleep(120)
#end loop
