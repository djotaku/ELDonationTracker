"""Contains the programming logic for the settings window in the GUI."""

import sys
import json
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog

from eldonationtracker.settings import *
from eldonationtracker import extralife_IO as extralife_IO


class MyForm(QDialog):
    """Class for the settings Window."""

    def __init__(self, participant_conf):
        """Init for the settings Window.

        Grabs the data from the participant.conf file and
        uses that to pre-populate the fields in the settings
        window.
        """
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.participant_conf = participant_conf
        (self.ExtraLifeID, self.textFolder,
         self.CurrencySymbol, self.TeamID, self.TrackerImage,
         self.DonationSound,
         self.donors_to_display) = participant_conf.get_GUI_values()
        self.ui.lineEditParticipantID.setText(self.ExtraLifeID)
        self.ui.labelTextFolder.setText(self.textFolder)
        self.ui.lineEditCurrencySymbol.setText(self.CurrencySymbol)
        self.ui.lineEditTeamID.setText(self.TeamID)
        self.ui.label_tracker_image.setText(self.TrackerImage)
        self.ui.label_sound.setText(self.DonationSound)
        self.ui.pushButtonRevert.clicked.connect(self.revert)
        self.ui.pushButtonSave.clicked.connect(self.save)
        self.ui.pushButton_persistentsave.clicked.connect(self.persistent_save)
        self.ui.pushButtonSelectFolder.clicked.connect(self._selectfolder)
        self.ui.pushButton_tracker_image.clicked.connect(lambda: self._selectfile("image"))
        self.ui.pushButton_sound.clicked.connect(lambda: self._selectfile("sound"))
        # self.ui.spinBox_DonorsToDisplay.valueChanged.connect(self.donorschanged)
        if self.donors_to_display is None:
            self.ui.spinBox_DonorsToDisplay.setValue(0)
        else:
            self.ui.spinBox_DonorsToDisplay.setValue(int(self.donors_to_display))

    def reload_config(self):
        """Reload the values from the config file.

        Called by gui.py before loading the settings window.
        """
        (self.ExtraLifeID, self.textFolder,
         self.CurrencySymbol, self.TeamID, self.TrackerImage,
         self.DonationSound, self.donors_to_display) = self.participant_conf.get_GUI_values()

    def revert(self):
        """
        Revert the values in the settings window.

        If the user made mistakes while editing the config this will
        take them back to the values since they opened the window.
        """
        self.ui.lineEditParticipantID.setText(self.ExtraLifeID)
        self.ui.labelTextFolder.setText(self.textFolder)
        self.ui.lineEditCurrencySymbol.setText(self.CurrencySymbol)
        self.ui.lineEditTeamID.setText(self.TeamID)
        self.ui.label_tracker_image.setText(self.TrackerImage)
        self.ui.label_sound.setText(self.DonationSound)
        if self.donors_to_display is None:
            self.ui.spinBox_DonorsToDisplay.setValue(0)
        else:
            self.ui.spinBox_DonorsToDisplay.setValue(int(self.donors_to_display))

    def _elements_to_save(self):
        participantID = self.ui.lineEditParticipantID.text()
        textfolder = self.ui.labelTextFolder.text()
        currencysymbol = self.ui.lineEditCurrencySymbol.text()
        trackerimage = self.ui.label_tracker_image.text()
        sound = self.ui.label_sound.text()
        version = self.participant_conf.get_version()
        donors_to_display = self.ui.spinBox_DonorsToDisplay.value()

        if self.ui.lineEditTeamID.text() == "":
            teamID = None
        else:
            teamID = self.ui.lineEditTeamID.text()
        config = {'Version': version, 'extralife_id': participantID,
                  'text_folder': textfolder, 'currency_symbol': currencysymbol,
                  'team_id': teamID, 'tracker_image': trackerimage,
                  'donation_sound': sound,
                  "donors_to_display": donors_to_display}
        return config

    def save(self):
        """Save the values in the window to participant.conf.

        Calls the write_config method from extralife_IO.ParticipantConf.
        """
        config = self._elements_to_save()
        self.participant_conf.write_config(config, True)

    def persistent_save(self):
        """Use xdg_config, saves a persistent config to the XDG spot."""
        config = self._elements_to_save()
        self.participant_conf.write_config(config, False)

    def _selectfolder(self):
        directory = QFileDialog.getExistingDirectory(self, "Get Folder")
        self.ui.labelTextFolder.setText(directory)

    def _selectfile(self, whichfile):
        the_file = QFileDialog.getOpenFileName(self, "Select File")
        if whichfile == "image":
            self.ui.label_tracker_image.setText(the_file[0])
        if whichfile == "sound":
            self.ui.label_sound.setText(the_file[0])


def main(participant_conf):
    """Launch the window."""
    w = MyForm(participant_conf)
    w.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
