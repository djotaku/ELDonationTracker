"""A window that displays the last donation. Useful during streaming."""

import sys
from PyQt5.QtWidgets import QDialog, QApplication, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import pyqtSlot, QUrl, Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

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
        # config stuff
        self.participant_conf = participant_conf
        self.folders = self.participant_conf.get_text_folder_only()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.scene = QGraphicsScene(self)
        self.pixmap = QtGui.QPixmap()
        self._loadimage()
        self.ui.graphicsView.setScene(self.scene)
        self.donation_player = QMediaPlayer()
        self._loadsound()
        self.ui.Donation_label.setTextColor(Qt.white)
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
        # want to also play a sound
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


def main(participant_conf):
    """Launch the window."""
    w = MyForm(participant_conf)
    w.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
