"""Contains the programming logic for the settings window in the GUI."""

import logging
from rich.logging import RichHandler
from rich import print

from PyQt5.QtWidgets import QDialog, QFileDialog, QFontDialog, QColorDialog, QMessageBox
from PyQt5.QtGui import QFont, QColor

from eldonationtracker.ui.settings import *
from eldonationtracker import base_api_url
from eldonationtracker.utils import extralife_io

# logging
LOG_FORMAT = '%(name)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, handlers=[RichHandler(markup=True, show_path=False)])
call_settings_log = logging.getLogger("call settings")


class MyForm(QDialog):
    """Class for the settings Window."""

    def __init__(self, participant_conf, tracker):
        """Init for the settings Window.

        Grabs the data from the participant.conf file and
        uses that to pre-populate the fields in the settings
        window.

        :param participant_conf: The participant configuration values.
        :type participant_conf: extralife_io.ParticipantConf
        :param tracker: A reference to the tracker.
        """
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.participant_conf = participant_conf
        self.tracker = tracker
        (self.ExtraLifeID, self.textFolder, self.CurrencySymbol, self.TeamID, self.TrackerImage, self.DonationSound,
         self.donors_to_display, self.font_family, self.font_size, self.font_italic,
         self.font_bold, self.font_color_value, self.tracker_background_color_value) = participant_conf.get_gui_values()
        if self.font_family:
            self.font = QFont()
            self.font.setFamily(self.font_family)
            self.font.setPointSize(self.font_size)
            self.font.setItalic(self.font_italic)
            self.font.setWeight(self.font_bold)
        if self.font_color_value:
            self.font_color = QColor()
            self.font_color.setRgb(self.font_color_value[0], self.font_color_value[1], self.font_color_value[2],
                                   self.font_color_value[3])
        if self.tracker_background_color_value:
            self.tracker_background_color = QColor()
            self.tracker_background_color.setRgb(self.tracker_background_color_value[0],
                                                 self.tracker_background_color_value[1],
                                                 self.tracker_background_color_value[2],
                                                 self.tracker_background_color_value[3])
        self.ui.lineEditParticipantID.setText(self.ExtraLifeID)
        self.ui.labelTextFolder.setText(self.textFolder)
        self.ui.lineEditCurrencySymbol.setText(self.CurrencySymbol)
        self.ui.lineEditTeamID.setText(self.TeamID)
        self.ui.label_tracker_image.setText(self.TrackerImage)
        self.ui.label_sound.setText(self.DonationSound)
        self.ui.pushButtonRevert.clicked.connect(self.revert)
        self.ui.pushButton_persistentsave.clicked.connect(self.persistent_save)
        self.ui.pushButtonSelectFolder.clicked.connect(self._select_folder)
        self.ui.pushButton_tracker_image.clicked.connect(lambda: self._select_file("image"))
        self.ui.pushButton_sound.clicked.connect(lambda: self._select_file("sound"))
        self.ui.pushButton_font.clicked.connect(self._change_font)
        self.ui.pushButton_font_color.clicked.connect(self._change_font_color)
        self.ui.pushButton_tracker_background.clicked.connect(self._change_tracker_bg_color)
        self.ui.pushButton_grab_image.clicked.connect(lambda: self._get_tracker_assets("image"))
        self.ui.pushButton_grab_sound.clicked.connect(lambda: self._get_tracker_assets("sound"))
        self.ui.pushButton_validate_participant_id.clicked.connect(lambda: self._validate_id("participant"))
        self.ui.pushButton_validate_team_id.clicked.connect(lambda: self._validate_id("team"))
        if self.donors_to_display is None:
            self.ui.spinBox_DonorsToDisplay.setValue(0)
        else:
            self.ui.spinBox_DonorsToDisplay.setValue(int(self.donors_to_display))

    def reload_config(self):
        """Reload the values from the config file.

        Called by ui.py before loading the settings window.
        """
        (self.ExtraLifeID, self.textFolder,
         self.CurrencySymbol, self.TeamID, self.TrackerImage,
         self.DonationSound, self.donors_to_display,
         self.font_family, self.font_size, self.font_italic, self.font_bold,
         self.font_color_value, self.tracker_background_color_value) = self.participant_conf.get_gui_values()

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
        participant_id = self.ui.lineEditParticipantID.text()
        text_folder = self.ui.labelTextFolder.text()
        currency_symbol = self.ui.lineEditCurrencySymbol.text()
        tracker_image = self.ui.label_tracker_image.text()
        sound = self.ui.label_sound.text()
        version = self.participant_conf.get_version()
        donors_to_display = self.ui.spinBox_DonorsToDisplay.value()
        try:
            font_family = self.font.family()
            font_size = self.font.pointSize()
            font_italic: bool = self.font.italic()
            font_bold: int = self.font.weight()
        except AttributeError:
            font_family = None
            font_size = None
            font_italic: bool = None
            font_bold: int = None
            font_color = None

        try:
            font_color = self.font_color.getRgb()
        except AttributeError:
            font_color = None

        try:
            tracker_background_color = self.tracker_background_color.getRgb()
        except AttributeError:
            tracker_background_color = None

        if self.ui.lineEditTeamID.text() == "":
            team_id = None
        else:
            team_id = self.ui.lineEditTeamID.text()
        config = {'Version': version, 'extralife_id': participant_id,
                  'text_folder': text_folder, 'currency_symbol': currency_symbol,
                  'team_id': team_id, 'tracker_image': tracker_image,
                  'donation_sound': sound,
                  "donors_to_display": donors_to_display,
                  "font_family": font_family, "font_size": font_size, "font_italic": font_italic,
                  "font_bold": font_bold, "font_color": font_color,
                  "tracker_background_color": tracker_background_color}
        return config

    def persistent_save(self):
        """Use xdg_config, saves a persistent config to the XDG spot."""
        config = self._elements_to_save()
        self.participant_conf.write_config(config, False)

    def _select_folder(self):
        directory = QFileDialog.getExistingDirectory(self, "Get Folder")
        self.ui.labelTextFolder.setText(directory)

    def _select_file(self, which_file):
        the_file = QFileDialog.getOpenFileName(self, "Select File")
        if which_file == "image":
            self.ui.label_tracker_image.setText(the_file[0])
        if which_file == "sound":
            self.ui.label_sound.setText(the_file[0])

    def _change_font(self):
        if self.font_family:
            font, ok = QFontDialog.getFont(self.font)
        else:
            font, ok = QFontDialog.getFont()
        if ok:
            self.tracker.set_font(font)
            self.font = font

    def _change_font_color(self):
        if self.font_color_value:
            col = QColorDialog.getColor(self.font_color)
        else:
            col = QColorDialog.getColor()
        self.font_color = col
        self.tracker.set_font_color(self.font_color)

    def _change_tracker_bg_color(self):
        if self.tracker_background_color_value:
            col = QColorDialog.getColor(self.tracker_background_color)
        else:
            col = QColorDialog.getColor()
        self.tracker_background_color = col
        self.tracker.set_background_color(self.tracker_background_color)

    def _get_tracker_assets(self, asset):
        file = self.participant_conf.get_tracker_assets(asset)
        if asset == "image":
            self.ui.label_tracker_image.setText(file)
        elif asset == "sound":
            self.ui.label_sound.setText(file)

    def _validate_id(self, id_type: str):
        call_settings_log.debug("[bold blue]Validating URL[/bold blue]")
        if id_type == "participant":
            url = f"{base_api_url}/participants/{self.ui.lineEditParticipantID.text()}"
            valid_url = extralife_io.validate_url(url)
            if valid_url:
                message_box = QMessageBox.information(self, "Participant ID Validation",
                                                      f"Able to reach {url}. Participant ID is valid.")
            else:
                message_box = QMessageBox.warning(self, "Participant ID Validation",
                                                  f"Could not reach {url}. Participant ID may be invalid.")
        elif id_type == "team":
            url = f"{base_api_url}/teams/{self.ui.lineEditTeamID.text()}"
            valid_url = extralife_io.validate_url(url)
            if valid_url:
                message_box = QMessageBox.information(self, "Team ID Validation",
                                                      f"Able to reach {url}. Team ID is valid.")
            else:
                message_box = QMessageBox.warning(self, "Team ID Validation",
                                                  f"Could not reach {url}. Team ID may be invalid.")


def main(participant_conf):
    """Launch the window."""
    window = MyForm(participant_conf)
    window.exec()