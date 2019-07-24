import sys
from PyQt5.QtWidgets import QDialog, QApplication, QGraphicsScene, QGraphicsPixmapItem
from tracker import *
from PyQt5.QtCore import pyqtSlot

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
        #self.pixmap.load("Engineer.png")
        item=QGraphicsPixmapItem(self.pixmap.scaledToHeight(131))
        self.scene.addItem(item)
        self.ui.graphicsView.setScene(self.scene)
        
    @pyqtSlot(bool)    
    def loadElements(self):
        print("load")
        self.pixmap.load("Engineer.png")



def main():
    w = MyForm()
    w.exec()
        

if __name__=="__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
