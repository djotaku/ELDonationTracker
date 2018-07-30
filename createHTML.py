import extralifedonations

def writetofile(info,filename):
    "Handles all the file writes"
    f = open(extralifedonations.textFolder+filename, 'w')
    f.write(info)
    f.close
    

def readfromfile(filename):
    f = open(extralifedonations.textFolder+filename, 'r')
    if f.mode == 'r':
        return f.read()
    f.close
    
class tracker():
    def __init__(self):
        page = "<HTML><HEAD><meta http-equiv='refresh' content='15'></HEAD><BODY></BODY></HTML>"
        writetofile(page, "tracker.html")

    def updatetrackerwithdonation(self):
        page = "<HTML><HEAD><meta http-equiv='refresh' content='15'></HEAD><BODY><h1>New donation from %s</h1> </BODY></HTML>" % readfromfile("LastDonorNameAmnt.txt")
        writetofile(page, "tracker.html")


    def updatetrackerafterdonation(self):
        page = "<HTML><HEAD><meta http-equiv='refresh' content='15'></HEAD><BODY></BODY></HTML>"
        writetofile(page, "tracker.html")

class MainPage():
    def __init__(self):
        page = "<HTML><HEAD><meta http-equiv='refresh' content='15'></HEAD><BODY></BODY></HTML>"
        writetofile(page, "mainpage.html")
    
    def updatemainpage(self):
        LastDonation = readfromfile("LastDonorNameAmnt.txt")
        TopDonation = readfromfile("TopDonorNameAmnt.txt")
        TotalRaised = readfromfile("totalRaised.txt")
        Goal = readfromfile("goal.txt")
        TotNumDonations = extralifedonations.CountDonors(extralifedonations.participantJSON)
        AvgDonation = " "
        TeamTotal = " "
        TeamGoal = " "
        TopTeamParticipant = " "
        RecentDonations = readfromfile("last5DonorNameAmts.txt")
        Top5TeamParticipants  = " "
        page = """<HTML><HEAD><meta http-equiv='refresh' content='15'></HEAD><BODY>
        
        Last Donation: %s
        <br>Top Donation: %s
        <br>Total Raised: %s
        <br>Goal: %s
        <br>Total Number of Donations: %s
        <br>Average Donation: %s
        <br>Team Total: %s
        <br>Team Goal: %s
        <br>Top Team Participant: %s
        <br>Recent Donations: %s
        <br>Top 5 Team Participants: %s
        
        </BODY></HTML>""" % (LastDonation, TopDonation, TotalRaised, Goal, TotNumDonations, AvgDonation, TeamTotal, TeamGoal, TopTeamParticipant, RecentDonations, Top5TeamParticipants)
        writetofile(page, "mainpage.html")
    
    
if __name__=="__main__":
    tracker1 = tracker()
    mainpage = MainPage()
