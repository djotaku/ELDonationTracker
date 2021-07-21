# type: ignore

"""The main GUI window."""

import logging

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QInputDialog

from PyQt5 import QtCore

from rich import print
from rich.logging import RichHandler
import sys
import webbrowser

from eldonationtracker.api import participant as participant
from eldonationtracker.ui import call_about as call_about, call_settings as call_settings, call_tracker as call_tracker, \
    main_gui as design
from eldonationtracker.utils import extralife_io as extralife_io
import eldonationtracker.utils.update_available

# logging
LOG_FORMAT = '%(name)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, handlers=[RichHandler(markup=True, show_path=False)])
GUI_log = logging.getLogger("main GUI")


class ELDonationGUI(QMainWindow, design.Ui_MainWindow):
    """The main ui Window."""

    def __init__(self):
        """Setup the GUI.

        Set up QTimers:
         1) to allow the text on the GUI to update without blocking the user from interacting with the GUI.
         2) to run the participant.py updates

        Then we instantiate the other windows:
        tracker and settings

        Finally, connect the buttons.
        """
        super(self.__class__, self).__init__()

        self.participant_conf = extralife_io.ParticipantConf()

        # deal with version mismatch
        self.version_mismatch = self.participant_conf.get_version_mismatch()
        self.version_check()

        self.setupUi(self)

        # timer to update the main text
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.setInterval(15000)  # milliseconds
        self.timer.timeout.connect(self.get_some_text)
        self.timer.start()

        # setup the participant
        self.my_participant = participant.Participant(self.participant_conf)
        self.participant_timer = QtCore.QTimer(self)
        self.participant_timer.setSingleShot(False)
        self.participant_timer.setInterval(15000)
        self.participant_timer.timeout.connect(self.my_participant.run)

        # instantiate the tracker so we can send signals
        self.tracker = call_tracker.MyForm(self.participant_conf, self.my_participant)

        # instantiate the settings
        self.call_settings = call_settings.MyForm(self.participant_conf, self.tracker)

        # instantiate About
        self.call_about = call_about.AboutProgram()

        # want to make sure file exists on new run
        self.folders = self.participant_conf.get_text_folder_only()

        # Connecting *almost* all the buttons to methods
        self.SettingsButton.clicked.connect(self.call_settings_button)
        self.TrackerButton.clicked.connect(self.call_tracker_button)
        self.ProgressBarButton.clicked.connect(self.dead_button)
        self.RefreshButton.clicked.connect(self.get_some_text)
        self.TestAlertButton.clicked.connect(self.test_alert)
        self.pushButtonRun.clicked.connect(self.run_button)
        self.pushButtonStop.clicked.connect(self.stop_button)

        # Menu connections
        self.actionQuit.triggered.connect(self.quit)
        self.actionDocumentation.triggered.connect(self.load_documentation)
        self.actionCheck_for_Update.triggered.connect(self.check_for_update)
        self.actionAbout.triggered.connect(self.show_about)

    def version_check(self):
        GUI_log.debug("[bold blue]Participant.conf version check![/bold blue]")
        if self.version_mismatch is True:
            GUI_log.debug("[bold magenta]There is a version mismatch[/bold magenta]")
            choices = ("Replace with Defaults", "Update on Save")
            choice, ok = QInputDialog.getItem(self, "Input Dialog",
                                              "You are using an old version of the configuration file.\n Choose "
                                              "what you would like to do.\n If you choose Update on Save, please "
                                              "click on the settings button, review the new options, and hit save.",
                                              choices, 0, False)
            if ok and choice:
                GUI_log.debug(f"[bold blue]You have chosen {choice}[/bold blue]")
                if choice == "Replace with Defaults":
                    self.participant_conf.get_github_config()
                    GUI_log.info("[bold blue]Settings have been replaced with the repo defaults.[/bold blue]")
                    self.participant_conf.reload_json()
                if choice == "Update on Save":
                    GUI_log.info("[bold blue]When you save the settings, you will be up to date[/bold blue]")
        else:
            GUI_log.debug("[bold green]Version is correct[/bold green] ")

    def test_alert(self):
        self.tracker.load_and_unload_test()

    def call_tracker_button(self):
        self.tracker.show()

    def call_settings_button(self):
        self.call_settings.reload_config()
        self.call_settings.show()
        # call_settings.main(self.participant_conf)

    # this is used for buttons that I haven't yet implemented
    @staticmethod
    def dead_button():
        GUI_log.info("[bold blue]not working yet[/bold blue]")

    @staticmethod
    def read_files(folders, files):
        try:
            f = open(f'{folders}/{files}', 'r', encoding='utf8')
            text = f.read()
            f.close()
            return text
        except FileNotFoundError:
            GUI_log.error(f"""[bold magenta]GUI Error:
                {folders}/{files} does not exist.
                Did you update the settings?
                Did you hit the 'run' button?[/bold magenta]
                """)

    def get_some_text(self):
        # For next refactoring, will use dict to make this just work as a loop
        # needs to be repeated in here to get new folder if config changes
        self.folders = self.participant_conf.get_text_folder_only()
        # Participant Info
        self.RecentDonations.setPlainText(self.read_files(self.folders, 'lastNDonationNameAmts.txt'))
        self.LastDonation.setPlainText(self.read_files(self.folders, 'LastDonationNameAmnt.txt'))
        self.TopDonation.setPlainText(self.read_files(self.folders, 'TopDonorNameAmnt.txt'))
        self.TotalRaised.setPlainText(self.read_files(self.folders, 'totalRaised.txt'))
        self.TotalNumDonations.setPlainText(self.read_files(self.folders, 'numDonations.txt'))
        self.Goal.setPlainText(self.read_files(self.folders, 'goal.txt'))
        self.AvgDonation.setPlainText(self.read_files(self.folders, 'averageDonation.txt'))
        try:
            avatar_url = QtCore.QUrl.fromLocalFile(self.folders + '/Participant_Avatar.html')
            self.participant_avatar.setUrl(avatar_url)
        except FileNotFoundError:
            GUI_log.warning("[bold blue] Participant Avatar not found. After running you should have it.[/bold blue]")

        # Team Info
        if self.participant_conf.get_if_in_team():
            self.label_TeamCaptain.setText(self.read_files(self.folders, 'Team_captain.txt'))
            self.label_TeamGoal.setText(self.read_files(self.folders, 'Team_goal.txt'))
            self.label_TeamNumDonations.setText(self.read_files(self.folders, 'Team_numDonations.txt'))
            self.label_TeamTotalRaised.setText(self.read_files(self.folders, 'Team_totalRaised.txt'))
            self.label_TopTeamParticipant.setText(self.read_files(self.folders, 'Team_TopParticipantNameAmnt.txt'))
            self.textBrowser_TeamTop5.setPlainText(self.read_files(self.folders, 'Team_Top5Participants.txt'))

    def run_button(self):
        GUI_log.info(f"[bold blue]Starting the participant run. But first, reloading config file.[/bold blue]")
        self.participant_conf.reload_json()
        # reload participant.conf in participant in case the user has changed settings
        self.my_participant.set_config_values()
        self.participant_timer.start()

    def stop_button(self):
        self.participant_timer.stop()

    def quit(self):
        """Quit the application.
        """
        self.participant_timer.stop()
        sys.exit()

    def load_documentation(self):
        try:
            webbrowser.open("https://eldonationtracker.readthedocs.io/en/latest/index.html", new=2)
        except webbrowser.Error:
            GUI_log.error("[bold red]Couldn't open documentation[/bold red]")
            message_box = QMessageBox.warning(self, "Documentation",
                                              "Could not load documentation. You may access in your browser at "
                                              "https://eldonationtracker.readthedocs.io/en/latest/index.html")

    def check_for_update(self):
        if eldonationtracker.utils.update_available.main():
            message_box = QMessageBox.information(self, "Check for Updates", "There is an update available.")
        else:
            message_box = QMessageBox.information(self, "Check for Updates", "You have the latest version.")

    def show_about(self):
        self.call_about.show()


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = ELDonationGUI()  # We set the form to be our ELDonationGUI (design)
    form.show()  # Show the form
    app.exec_()  # and execute the app


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function
