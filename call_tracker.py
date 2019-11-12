import sys
from PyQt5.QtWidgets import QDialog, QApplication, QGraphicsScene, QGraphicsPixmapItem
from tracker import *
from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

import IPC


class MyForm(QDialog):
    def __init__(self, participant_conf):
        super().__init__()
        # config stuff
        self.participant_conf = participant_conf
        self.folders = self.participant_conf.get_text_folder_only()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.scene = QGraphicsScene(self)
        self.pixmap = QtGui.QPixmap()
        self.loadimage()
        self.ui.graphicsView.setScene(self.scene)
        self.donation_player = QMediaPlayer()
        self.loadsound()
        # timer to update the main text
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.setInterval(20000)  # milliseconds
        self.timer.timeout.connect(self.loadAndUnload)
        self.timer.start()

    def loadimage(self):
        self.tracker_image = self.participant_conf.get_tracker_image()
        self.pixmap.load(self.tracker_image)
        self.item = QGraphicsPixmapItem(self.pixmap.scaledToHeight(131))

    def loadsound(self):
        sound_to_play = self.participant_conf.get_tracker_sound()
        self.donation_sound= QMediaContent(QUrl.fromLocalFile(sound_to_play))
        self.donation_player.setMedia(self.donation_sound)

    def loadAndUnloadTest(self):
        self.loadimage()
        self.loadElements()
        self.loadsound()
        self.donation_player.play()
        unloadtimer = QtCore.QTimer(self)
        unloadtimer.setSingleShot(True)
        unloadtimer.setInterval(5000)  # milliseconds
        unloadtimer.timeout.connect(self.unloadElements)
        unloadtimer.start()

    def loadAndUnload(self):
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
            self.loadimage()
            self.loadElements()
            self.loadsound()
            self.donation_player.play()
            unloadtimer = QtCore.QTimer(self)
            unloadtimer.setSingleShot(True)
            unloadtimer.setInterval(5000)  # milliseconds
            unloadtimer.timeout.connect(self.unloadElements)
            unloadtimer.start()

    def loadElements(self):
        self.scene.addItem(self.item)
        # want to also play a sound
        try:
            with open(f'{self.folders}/LastDonorNameAmnt.txt') as file:
                donorAndAmt = file.read()
                file.close
            self.ui.Donation_label.setText(donorAndAmt)
        except:
            self.ui.Donation_label.setText("TEST 1...2...3...")

    def unloadElements(self):
        self.scene.removeItem(self.item)
        self.ui.Donation_label.setText("")
        IPC.writeIPC(self.folders, "0")


def main(participant_conf):
    w = MyForm(participant_conf)
    w.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
