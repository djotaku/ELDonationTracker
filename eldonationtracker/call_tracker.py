"""A window that displays the last donation. Useful during streaming."""

import sys
from PyQt5.QtWidgets import QDialog, QApplication, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QFont, QColor

from eldonationtracker.tracker import *
from eldonationtracker import ipc as ipc


class MyForm(QDialog):
    """The class to hold the tracker window."""

    def __init__(self, participant_conf):
        """Set up the window.

        Loads in the image and sound file the user specified in the
        participant.conf settings file.
        """
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # config stuff
        self.participant_conf = participant_conf
        self.folders = self.participant_conf.get_text_folder_only()
        (self.font_family, self.font_size, self.font_italic, self.font_bold,
         self.font_color_value) = self.participant_conf.get_font_info()
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
        self._loadimage()
        self.ui.graphicsView.setScene(self.scene)
        self.donation_player = QMediaPlayer()
        self._loadsound()
        # timer to update the main text
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.setInterval(20000)  # milliseconds
        self.timer.timeout.connect(self._loadAndUnload)
        self.timer.start()

    def _loadimage(self):
        self.tracker_image = self.participant_conf.get_tracker_image()
        self.pixmap.load(self.tracker_image)
        self.item = QGraphicsPixmapItem(self.pixmap.scaledToHeight(131))

    def _loadsound(self):
        sound_to_play = self.participant_conf.get_tracker_sound()
        self.donation_sound= QMediaContent(QUrl.fromLocalFile(sound_to_play))
        self.donation_player.setMedia(self.donation_sound)

    def loadAndUnloadTest(self):
        """Trigger the tracker functionality.

        This causes the image and sound to load so that the
        user can test to see how it's going to look on their OBS
        or XSplit screen as well as to make sure they can hear
        the sound. Called by gui.py.
        """
        self._loadimage()
        self._loadElements()
        self._loadsound()
        self.donation_player.play()
        unloadtimer = QtCore.QTimer(self)
        unloadtimer.setSingleShot(True)
        unloadtimer.setInterval(5000)  # milliseconds
        unloadtimer.timeout.connect(self._unloadElements)
        unloadtimer.start()

    def _loadAndUnload(self):
        self.folders = self.participant_conf.get_text_folder_only()
        IPC = "0"
        try:
            with open(f'{self.folders}/trackerIPC.txt') as file:
                IPC = file.read(1)
                file.close()
        except:
            print("""tackerIPC.txt not found.
                Have you updated the settings?
                Have you hit the 'run' button?""")
        if IPC == "1":
            self._loadimage()
            self._loadElements()
            self._loadsound()
            self.donation_player.play()
            unloadtimer = QtCore.QTimer(self)
            unloadtimer.setSingleShot(True)
            unloadtimer.setInterval(5000)  # milliseconds
            unloadtimer.timeout.connect(self._unloadElements)
            unloadtimer.start()

    def _loadElements(self):
        self.scene.addItem(self.item)
        try:
            with open(f'{self.folders}/LastDonationNameAmnt.txt') as file:
                donorAndAmt = file.read()
                file.close
            self.ui.Donation_label.setText(donorAndAmt)
        except FileNotFoundError:
            self.ui.Donation_label.setText("TEST 1...2...3...")

    def _unloadElements(self):
        self.scene.removeItem(self.item)
        self.ui.Donation_label.setText("")
        ipc.writeIPC(self.folders, "0")

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
