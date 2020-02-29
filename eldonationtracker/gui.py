"""The main GUI window."""

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QInputDialog

from PyQt5 import QtCore

from PyQt5.QtCore import Qt, pyqtSignal  # need Qt?

import sys
import threading
import shutil
import webbrowser

from eldonationtracker import design as design
from eldonationtracker import extralifedonations as extralifedonations
from eldonationtracker import call_about as call_about
from eldonationtracker import call_tracker as call_tracker
from eldonationtracker import call_settings as call_settings
from eldonationtracker import extralife_IO as extralife_IO
from eldonationtracker import ipc as ipc
import eldonationtracker.utils.update_available


class ELDonationGUI(QMainWindow, design.Ui_MainWindow):
    """The main gui Window."""

    def __init__(self):
        """Setup the GUI.

        We have a QTimer to allow the text on the GUI
        to update without blocking the user from interacting
        with the GUI.

        Then we instantiate the other windows:
        tracker and settings
        And connect the buttons.
        """
        super(self.__class__, self).__init__()

        self.participant_conf = extralife_IO.ParticipantConf()

        # deal with version mismatch
        self.version_mismatch = self.participant_conf.get_version_mismatch()
        self.version_check()

        self.setupUi(self)

        # timer to update the main text
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.setInterval(15000)  # milliseconds
        self.timer.timeout.connect(self.getsomeText)
        self.timer.start()

        # instantiate the tracker so we can send signals
        self.tracker = call_tracker.MyForm(self.participant_conf)

        # instantiate the settings
        self.call_settings = call_settings.MyForm(self.participant_conf)
        
        # instantiate About
        self.call_about = call_about.about_program()

        # want to make sure file exists on new run
        self.folders = self.participant_conf.get_text_folder_only()
        ipc.writeIPC(self.folders, "0")

        # Connecting *almost* all the buttons to methods
        self.SettingsButton.clicked.connect(self.callSettings)
        self.TrackerButton.clicked.connect(self.callTracker)
        self.ProgressBarButton.clicked.connect(self.deadbuton)
        self.RefreshButton.clicked.connect(self.getsomeText)
        self.TestAlertButton.clicked.connect(self.testAlert)
        self.pushButtonRun.clicked.connect(self.runbutton)
        self.pushButtonStop.clicked.connect(self.stopbutton)

        # Menu connections
        self.thread_running = False
        self.actionQuit.triggered.connect(self.quit)
        self.actionDocumentation.triggered.connect(self.load_documentation)
        self.actionCheck_for_Update.triggered.connect(self.check_for_update)
        self.actionAbout.triggered.connect(self.show_about)

    def version_check(self):
        print("Participant.conf version check!")
        if self.version_mismatch is True:
            print("There is a version mismatch")
            choices = ("Replace with Defaults", "Update on Save")
            choice, ok = QInputDialog.getItem(self, "Input Dialog",
                                              "You are using an old version of the configuration file.\n Choose what you would like to do.\n If you choose Update on Save, please click on teh settings button, review the new options, and hit save.", choices, 0,
                                              False)
            if ok and choice:
                print(f"You have chosen {choice}")
                if choice == "Replace with Defaults":
                    shutil.move("participant.conf", "participant.conf.bak")
                    print("Your settings were backed up to participant.conf.bak")
                    shutil.copy("backup_participant.conf", "participant.conf")
                    print("Settings have been replaced with the repo defaults.")
                    self.participant_conf.reload_JSON()
                if choice == "Update on Save":
                    print("When you save the settings, you will be up to date")
        else:
            print("Version is correct")

    def testAlert(self):
        self.tracker.loadAndUnloadTest()

    def callTracker(self):
        self.tracker.show()

    def callSettings(self):
        self.call_settings.reload_config()
        self.call_settings.show()
        # call_settings.main(self.participant_conf)

    # this is used for buttons that I haven't yet implemented
    def deadbuton(self):
        print("not working yet")

    def readFiles(self, folders, files):
        try:
            f = open(f'{folders}/{files}', 'r')
            text = f.read()
            f.close()
            return text
        except FileNotFoundError:
            print(f"""GUI Error:
                {folders}/{files} does not exist.
                Did you update the settings?
                Did you hit the 'run' button?
                """)

    def getsomeText(self):
        # For next refactoring, will use dict to make this just work as a loop
        # needs to be repeated in here to get new folder if config changes
        self.folders = self.participant_conf.get_text_folder_only()
        # Participant Info
        self.RecentDonations.setPlainText(self.readFiles(self.folders,
                                                         'lastNDonationNameAmts.txt'))
        self.LastDonation.setPlainText(self.readFiles(self.folders,
                                                      'LastDonationNameAmnt.txt'))
        self.TopDonation.setPlainText(self.readFiles(self.folders,
                                                     'TopDonorNameAmnt.txt'))
        self.TotalRaised.setPlainText(self.readFiles(self.folders,
                                                     'totalRaised.txt'))
        self.TotalNumDonations.setPlainText(self.readFiles(self.folders,
                                                           'numDonations.txt'))
        self.Goal.setPlainText(self.readFiles(self.folders, 'goal.txt'))
        self.AvgDonation.setPlainText(self.readFiles(self.folders,
                                                     'averageDonation.txt'))
        # Team Info
        if self.participant_conf.get_if_in_team():
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
        self.thread_running = True
        self.thread1 = donationGrabber(self.participant_conf)
        self.thread1.start()

    def stopbutton(self):
        self.thread1.stop()

    def quit(self):
        """Quit the application.

        First need to stop the thread running the CLI code.

        .. warning: This will change when the threading code is removed.
        """
        if self.thread_running:
            self.stopbutton()
        sys.exit()

    def load_documentation(self):
        try:
            webbrowser.open("https://eldonationtracker.readthedocs.io/en/latest/index.html", new=2)
        except webbrowser.Error:
            print("couldn't open documentation")
            message_box = QMessageBox.warning(self, "Documentation", "Could not load documentation. You may access in your browser at https://eldonationtracker.readthedocs.io/en/latest/index.html")

    def check_for_update(self):
        if eldonationtracker.utils.update_available.main():
            message_box = QMessageBox.information(self, "Check for Updates", "There is an update available.")
        else:
            message_box = QMessageBox.information(self, "Check for Updates", "You have the latest version.")

    def show_about(self):
        self.call_about.show()


class donationGrabber (threading.Thread):
    counter = 0

    def __init__(self, participant_conf):
        threading.Thread.__init__(self)
        self.counter = 0
        self.participant_conf = participant_conf

    def run(self):
        print(f"Starting {self.name}. But first, reloading config file.")
        self.participant_conf.reload_JSON()
        self.p = extralifedonations.Participant(self.participant_conf)
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
