""" Contains programming logic for the about window in the GUI."""

from PyQt5.QtWidgets import QDialog

from eldonationtracker.ui.about import *


class AboutProgram(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton_OK.clicked.connect(self.ok_clicked)

    def ok_clicked(self):
        self.close()


def main():
    w = AboutProgram()
    w.exec()
