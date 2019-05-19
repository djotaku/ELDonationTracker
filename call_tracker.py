import sys
from PyQt5.QtWidgets import QDialog, QApplication, QGraphicsScene, QGraphicsPixmapItem
from tracker import *

class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.scene = QGraphicsScene(self)
        pixmap = QtGui.QPixmap()
        pixmap.load("Engineer.png")
        item=QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)
        self.ui.graphicsView.setScene(self.scene)
        self.show()

def main():
    w = MyForm()
    w.exec()
        

if __name__=="__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
