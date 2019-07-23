#should change from line edits to labels

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

import design, sys, threading

import extralifedonations

import call_tracker, call_settings

class ELDonationGUI(QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Super allows us to access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined
        
        self.getsomeText() #this needs some work to not execute right away or at least try/catch
        
        self.SettingsButton.clicked.connect(self.callSettings)
        self.TrackerButton.clicked.connect(self.callTracker)
        self.ProgressBarButton.clicked.connect(self.deadbuton)
        self.RefreshButton.clicked.connect(self.getsomeText)
        self.TestAlertButton.clicked.connect(self.deadbuton)
        self.pushButtonRun.clicked.connect(self.runbutton)
        self.pushButtonStop.clicked.connect(self.stopbutton)
    
    def callTracker(self):
        call_tracker.main()
        
    def callSettings(self):
        call_settings.main()
    
    def deadbuton(self):
        print("button not yet working")
    
    def getsomeText(self):
        f = open('/home/ermesa/Dropbox/ELtracker/last5DonorNameAmts.txt', 'r') #these paths need to be changed to read from the config file. Actually - should be an action in init that creates a variable that can be put in all of these. 
        text=f.read()
        self.RecentDonations.setPlainText(text)
        f.close()
        f = open('/home/ermesa/Dropbox/ELtracker/LastDonorNameAmnt.txt','r')
        text=f.read()
        self.LastDonation.setPlainText(text)
        f.close()
        f = open('/home/ermesa/Dropbox/ELtracker/TopDonorNameAmnt.txt','r')
        text=f.read()
        self.TopDonation.setPlainText(text)
        f.close()
        f = open('/home/ermesa/Dropbox/ELtracker/totalRaised.txt','r')
        text=f.read()
        self.TotalRaised.setPlainText(text)
        f.close()
        f = open('/home/ermesa/Dropbox/ELtracker/numDonations.txt','r')
        text=f.read()
        self.TotalNumDonations.setPlainText(text)
        f.close()
        f = open('/home/ermesa/Dropbox/ELtracker/goal.txt','r')
        text=f.read()
        self.Goal.setPlainText(text)
        f.close()
        f = open('/home/ermesa/Dropbox/ELtracker/averageDonation.txt','r')
        text=f.read()
        self.AvgDonation.setPlainText(text)
        f.close()
    
    def runbutton(self):
        print("run button")
        #need to add some code to keep it from starting more than one thread. 
        self.thread1=donationGrabber()
        #self.thread2=updateText(self)
        self.thread1.start()
        #self.thread2.start()
        
    def stopbutton(self):
        self.thread1.stop() 

class donationGrabber (threading.Thread):
    counter = 0
    def __init__(self):
        threading.Thread.__init__(self)
        self.counter=0
    def run(self):
        print("Starting " + self.name)
        self.p = extralifedonations.Participant()
        self.p.run()
    def stop(self):
        self.p.stop()

class updateText (threading.Thread):
    counter = 0
    def __init__(self,parent):
        threading.Thread.__init__(self)
        self.counter=0
        self.parent=parent
    def run(self):
        print("Starting " + self.name)
        self.p = self.parent.getsomeText()
        self.p.run()
    def stop(self):
        self.p.stop()

def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = ELDonationGUI()                 # We set the form to be our ELDonationGUI (design)
    form.show()                         # Show the form
    self.thread2=updateText(app)
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function
