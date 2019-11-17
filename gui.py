#should change from line edits to labels

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from PyQt5 import QtCore

from PyQt5.QtCore import Qt, pyqtSignal  # need Qt?

import design
import sys
import threading

import extralifedonations
import call_tracker
import call_settings
import extralife_IO
import IPC

# setup config file
participant_conf = extralife_IO.ParticipantConf()


class ELDonationGUI(QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        # Super allows us to access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined

        # timer to update the main text
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.setInterval(15000)  # milliseconds
        self.timer.timeout.connect(self.getsomeText)
        self.timer.start()

        # instantiate the tracker so we can send signals
        self.tracker = call_tracker.MyForm(participant_conf)

        # want to make sure file exists on new run
        self.folders = participant_conf.get_text_folder_only()
        IPC.writeIPC(self.folders, "0")

        # Connecting all the buttons to methods
        self.SettingsButton.clicked.connect(self.callSettings)
        self.TrackerButton.clicked.connect(self.callTracker)
        self.ProgressBarButton.clicked.connect(self.deadbuton)
        self.RefreshButton.clicked.connect(self.getsomeText)
        self.TestAlertButton.clicked.connect(self.testAlert)
        self.pushButtonRun.clicked.connect(self.runbutton)
        self.pushButtonStop.clicked.connect(self.stopbutton)
        
    def testAlert(self):
        self.tracker.loadAndUnloadTest()
    
    def callTracker(self):
        self.tracker.show()
        
    def callSettings(self):
        call_settings.main(participant_conf)
    
    # this is used for buttons that I haven't yet implemented
    def deadbuton(self):
        print("not working yet")
    
    def readFiles(self, folders, files):
        try:
            f = open(f'{folders}/{files}', 'r') 
            text = f.read()
            f.close()
            return text
        except:
            print("""GUI Error:
                File does not exist.
                Did you update the settings?
                Did you hit the 'run' button?
                """)

    def getsomeText(self):
        # For next refactoring, will use dict to make this just work as a loop
        self.RecentDonations.setPlainText(self.readFiles(self.folders,
                                                         'last5DonorNameAmts.txt'))
        self.LastDonation.setPlainText(self.readFiles(self.folders,
                                                      'LastDonorNameAmnt.txt'))
        self.TopDonation.setPlainText(self.readFiles(self.folders,
                                                     'TopDonorNameAmnt.txt'))
        self.TotalRaised.setPlainText(self.readFiles(self.folders,
                                                     'totalRaised.txt'))
        self.TotalNumDonations.setPlainText(self.readFiles(self.folders,
                                                           'numDonations.txt'))
        self.Goal.setPlainText(self.readFiles(self.folders, 'goal.txt'))
        self.AvgDonation.setPlainText(self.readFiles(self.folders,
                                                     'averageDonation.txt'))
        self.label_TeamCaptain.setText(self.readFiles(self.folders,
                                                      'Team_captain.txt'))
        self.label_TeamGoal.setText(self.readFiles(self.folders, 'Team_goal.txt'))
        self.label_TeamNumDonations.setText(self.readFiles(self.folders,
                                                           'Team_numDonations.txt'))
        self.label_TeamTotalRaised.setText(self.readFiles(self.folders,
                                                          'Team_totalRaised.txt'))
        self.label_TopTeamParticipant.setText(self.readFiles(self.folders, 'Team_TopParticipantNameAmnt.txt'))
        self.textBrowser_TeamTop5.setPlainText(self.readFiles(self.folders, 'Team_Top5Participants.txt'))

    def runbutton(self):
        print("run button")
        # need to add some code to keep it from starting more than one thread. 
        self.thread1 = donationGrabber()
        self.thread1.start()

    def stopbutton(self):
        self.thread1.stop() 


class donationGrabber (threading.Thread):
    counter = 0

    def __init__(self):
        threading.Thread.__init__(self)
        self.counter = 0

    def run(self):
        print(f"Starting {self.name}. But first, reloading config file.")
        participant_conf.reload_JSON()
        self.p = extralifedonations.Participant(participant_conf)
        self.p.run()

    def stop(self):
        self.p.stop()


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = ELDonationGUI()   # We set the form to be our ELDonationGUI (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function
