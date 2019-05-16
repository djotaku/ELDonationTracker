#should change from line edits to labels

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

import design, sys

import call_tracker, call_settings

class ExampleApp(QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Super allows us to access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined
        self.getsomeText()
        
        self.SettingsButton.clicked.connect(self.callSettings)
        self.TrackerButton.clicked.connect(self.callTracker)
        self.ProgressBarButton.clicked.connect(self.deadbuton)
        self.RefreshButton.clicked.connect(self.getsomeText)
        self.TestAlertButton.clicked.connect(self.deadbuton)
    
    def callTracker(self):
        call_tracker.main()
        
    def callSettings(self):
        call_settings.main()
    
    def deadbuton(self):
        print("button not yet working")
    
    def getsomeText(self):
        f = open('/home/ermesa/Dropbox/ELtracker/last5DonorNameAmts.txt', 'r')
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

def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = ExampleApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function
