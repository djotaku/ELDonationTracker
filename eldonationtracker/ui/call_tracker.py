"""A window that displays the last donation. Useful during streaming."""

import logging
from rich.logging import RichHandler  # type ignore

from PyQt5.QtWidgets import QDialog, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent  # type: ignore
from PyQt5.QtGui import QFont, QColor

from eldonationtracker.ui.tracker import *

# logging
LOG_FORMAT = '%(name)s: %(message)s'
call_tracker_log = logging.getLogger("Call_Tracker")
call_tracker_log.setLevel(logging.INFO)


class MyForm(QDialog):
    """The class to hold the tracker window."""

    def __init__(self, participant_conf, participant):
        """Set up the window.

        Loads in the image and sound file the user specified in the
        participant.conf settings file.
        """
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # config stuff
        self.participant_conf = participant_conf
        self.participant = participant
        self.folders = self.participant_conf.get_text_folder_only()
        (self.font_family, self.font_size, self.font_italic, self.font_bold,
         self.font_color_value) = self.participant_conf.get_font_info()
        if self.font_family:
            self.font = QFont()
            self.font.setFamily(self.font_family)
            self.font.setPointSize(self.font_size)
            self.font.setItalic(self.font_italic)
            self.font.setWeight(self.font_bold)
            self.ui.Donation_label.setFont(self.font)
        if self.font_color_value:
            self.font_color = QColor()
            self.font_color.setRgb(self.font_color_value[0], self.font_color_value[1], self.font_color_value[2],
                                   self.font_color_value[3])
            self.ui.Donation_label.setTextColor(self.font_color)
        self.tracker_background_color_value = participant_conf.get_tracker_background_color()
        if self.tracker_background_color_value:
            self.tracker_background_color = QColor()
            self.tracker_background_color.setRgb(self.tracker_background_color_value[0],
                                                 self.tracker_background_color_value[1],
                                                 self.tracker_background_color_value[2],
                                                 self.tracker_background_color_value[3])
            self.ui.graphicsView.setBackgroundBrush(self.tracker_background_color)
        self.scene = QGraphicsScene(self)
        self.pixmap = QtGui.QPixmap()
        self._load_image()
        self.ui.graphicsView.setScene(self.scene)
        self.donation_player = QMediaPlayer()
        self._load_sound()
        # timer to update the main text
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.setInterval(15000)  # milliseconds
        self.timer.timeout.connect(self._load_and_unload)
        self.timer.start()

    def _load_image(self):
        self.tracker_image = self.participant_conf.get_tracker_image()
        self.pixmap.load(self.tracker_image)
        self.item = QGraphicsPixmapItem(self.pixmap.scaledToHeight(131))

    def _load_sound(self):
        sound_to_play = self.participant_conf.get_tracker_sound()
        self.donation_sound = QMediaContent(QUrl.fromLocalFile(sound_to_play))
        self.donation_player.setMedia(self.donation_sound)

    def _load_and_unload_helper(self):
        """Used both by the test code and the actual load and unload code."""
        call_tracker_log.debug("The load and unload helper was called.")
        self._load_image()
        self._load_elements()
        self._load_sound()
        self.donation_player.play()
        unload_timer = QtCore.QTimer(self)
        unload_timer.setSingleShot(True)
        unload_timer.setInterval(5000)  # milliseconds
        unload_timer.timeout.connect(self._unload_elements)
        unload_timer.start()

    def load_and_unload_test(self):
        """Trigger the tracker functionality.

        This causes the image and sound to load so that the
        user can test to see how it's going to look on their OBS
        or XSplit screen as well as to make sure they can hear
        the sound. Called by ui.py.
        """
        self._load_and_unload_helper()

    def _load_and_unload(self):
        self.folders = self.participant_conf.get_text_folder_only()
        call_tracker_log.debug("Checking if there are new donations.")
        if self.participant.new_donation:
            call_tracker_log.debug("There WAS a new donation!!!")
            self._load_and_unload_helper()

    def _load_elements(self):
        self.scene.addItem(self.item)
        try:
            with open(f'{self.folders}/LastDonationNameAmnt.txt') as file:
                donor_and_amt = file.read()
            self.ui.Donation_label.setText(donor_and_amt)
        except FileNotFoundError:
            self.ui.Donation_label.setText("TEST 1...2...3...")

    def _unload_elements(self):
        self.scene.removeItem(self.item)
        self.ui.Donation_label.setText("")
        self.participant.new_donation = False

    def set_font(self, font):
        self.ui.Donation_label.setFont(font)

    def set_font_color(self, font_color):
        self.ui.Donation_label.setTextColor(font_color)

    def set_background_color(self, color):
        self.ui.graphicsView.setBackgroundBrush(color)


def main(participant_conf):
    """Launch the window."""
    window = MyForm(participant_conf)
    window.exec()
