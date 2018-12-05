class tracker:
    
    def writetofile(self,info,filename):
        "Handles all the file writes"
        f = open(self.textFolder+filename, 'w')
        f.write(info)
        f.close
        
    def readfromfile(self,filename):
        f = open(self.textFolder+filename, 'r')
        if f.mode == 'r':
            return f.read()
        f.close   

    def __init__(self, textFolder):
        self.textFolder=textFolder
        page = "<HTML><HEAD><meta http-equiv='refresh' content='15'></HEAD><BODY></BODY></HTML>"
        self.writetofile(page, "tracker.html")

    def updatetrackerwithdonation(self):
        page = "<HTML><HEAD><meta http-equiv='refresh' content='15'></HEAD><BODY><h1>New donation from %s</h1> </BODY></HTML>" % self.readfromfile("LastDonorNameAmnt.txt")
        self.writetofile(page, "tracker.html")

    def updatetrackerafterdonation(self):
        page = "<HTML><HEAD><meta http-equiv='refresh' content='15'></HEAD><BODY></BODY></HTML>"
        self.writetofile(page, "tracker.html")

class MainPage:
    
    def writetofile(self,info,filename):
        "Handles all the file writes"
        f = open(self.textFolder+filename, 'w')
        f.write(info)
        f.close
        
    def readfromfile(self,filename):
        f = open(self.textFolder+filename, 'r')
        if f.mode == 'r':
            return f.read()
        f.close   
    
    
    def __init__(self, textFolder):
        self.textFolder=textFolder
        LastDonation = self.readfromfile("LastDonorNameAmnt.txt")
        TopDonation = self.readfromfile("TopDonorNameAmnt.txt")
        TotalRaised = self.readfromfile("totalRaised.txt")
        Goal = self.readfromfile("goal.txt")
        TotNumDonations = self.readfromfile("numDonations.txt")
        AvgDonation = self.readfromfile("averageDonation.txt")
        TeamTotal = "Needs a function in extralifedonations to write to a file"
        TeamGoal = "Needs a function in extralifedonations to write to a file"
        TopTeamParticipant = "Needs a function in extralifedonations to write to a file"
        RecentDonations = self.readfromfile("last5DonorNameAmtsMessageHorizontal.txt")
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
        self.writetofile(page, "mainpage.html")
    
    
if __name__=="__main__":
    tracker1 = tracker("/home/ermesa/Dropbox/ELtracker/")
    mainpage = MainPage("/home/ermesa/Dropbox/ELtracker/")
