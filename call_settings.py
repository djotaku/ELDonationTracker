import sys
import json
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from settings import *

import extralife_IO


class MyForm(QDialog):
    def __init__(self, participant_conf):
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
        self.ui.pushButtonSelectFolder.clicked.connect(self.selectfolder)
        self.ui.pushButton_tracker_image.clicked.connect(lambda: self.selectfile("image"))
        self.ui.pushButton_sound.clicked.connect(lambda: self.selectfile("sound"))
        #self.ui.spinBox_DonorsToDisplay.valueChanged.connect(self.donorschanged)
        if self.donors_to_display is None:
            self.ui.spinBox_DonorsToDisplay.setValue(0)
        else:
            self.ui.spinBox_DonorsToDisplay.setValue(int(self.donors_to_display))

    def reload_config(self):
        (self.ExtraLifeID, self.textFolder,
         self.CurrencySymbol, self.TeamID, self.TrackerImage,
         self.DonationSound, self.donors_to_display) = self.participant_conf.get_GUI_values()

    def revert(self):
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
        config = self._elements_to_save()
        self.participant_conf.write_config(config, True)

    def persistent_save(self):
        config = self._elements_to_save()
        self.participant_conf.write_config(config, False)

    def selectfolder(self):
        directory = QFileDialog.getExistingDirectory(self, "Get Folder")
        self.ui.labelTextFolder.setText(directory)

    def selectfile(self, whichfile):
        the_file = QFileDialog.getOpenFileName(self, "Select File")
        if whichfile == "image":
            self.ui.label_tracker_image.setText(the_file[0])
        if whichfile == "sound":
            self.ui.label_sound.setText(the_file[0])


def main(participant_conf):
    w = MyForm(participant_conf)
    w.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
