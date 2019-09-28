import sys
from PyQt5.QtWidgets import QDialog, QApplication, QGraphicsScene, QGraphicsPixmapItem
from tracker import *
from PyQt5.QtCore import pyqtSlot

import readparticipantconf
import IPC

# *** For GUI release, need to use QTimer and a function to check whether there's been a donation
# and update this window
#to remove the item call scene.removeItem()

class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.scene = QGraphicsScene(self)
        self.pixmap = QtGui.QPixmap()
        self.pixmap.load("Engineer.png")
        self.item=QGraphicsPixmapItem(self.pixmap.scaledToHeight(131))
        self.ui.graphicsView.setScene(self.scene)
        
        #timer to update the main text
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.setInterval(20000) #milliseconds
        self.timer.timeout.connect(self.loadAndUnload) 
        self.timer.start()
    
    def loadAndUnloadTest(self):
        self.loadElements()
        unloadtimer = QtCore.QTimer(self)
        unloadtimer.setSingleShot(True)
        unloadtimer.setInterval(5000) #milliseconds
        unloadtimer.timeout.connect(self.unloadElements)
        unloadtimer.start()
    
    def loadAndUnload(self):
        folders = readparticipantconf.textfolderOnly()
        #this needs to be moved to a try/except
        try:
            with open(f'{folders}/trackerIPC.txt') as file:
                IPC = file.read(1)
                print(f'IPC is {IPC}')
                file.close()
        except:
            print("This shouldn't be happpening!")
        if IPC == "1": 
            print("Donation changed IPC value!")
            self.loadElements()
            unloadtimer = QtCore.QTimer(self)
            unloadtimer.setSingleShot(True)
            unloadtimer.setInterval(5000) #milliseconds
            unloadtimer.timeout.connect(self.unloadElements)
            unloadtimer.start()
    
    def loadElements(self):
        print("load")
        self.scene.addItem(self.item)
        #want to also play a sound
        folders = readparticipantconf.textfolderOnly()
        #this needs to be moved to a try/except
        try:
            with open(f'{folders}/LastDonorNameAmnt.txt') as file:
                donorAndAmt = file.read()
                file.close
            self.ui.Donation_label.setText(donorAndAmt)
        except:
            self.ui.Donation_label.setText("TEST 1...2...3...")
        
    def unloadElements(self):
        print('unload')
        self.scene.removeItem(self.item)
        self.ui.Donation_label.setText("")
        IPC.writeIPC("0")

        

def main():
    w = MyForm()
    w.exec()
        

if __name__=="__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
