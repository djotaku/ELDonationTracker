"""Contains the programming logic for the settings window in the GUI."""

import logging

from PyQt5.QtWidgets import QDialog

from eldonationtracker import file_logging
from eldonationtracker.ui.logs import *

# logging
call_logs_log = logging.getLogger("logs")
call_logs_log.addHandler(file_logging)


class MyForm(QDialog):
    """Class for the settings Window."""

    def __init__(self):
        """

        """
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.logs.setText("Within 15 seconds will attempt to set with log content....")

        # timer to update the main log
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.setInterval(15000)  # milliseconds
        self.timer.timeout.connect(self.update_log)
        self.timer.start()

        self.ui.copy.clicked.connect(self.copy_clipboard)

    def update_log(self):
        try:
            with open("eldonationtracker_log.txt", 'r') as file:
                log = file.read()
                self.ui.logs.setText(log)
        except FileNotFoundError:
            call_logs_log.error("Couldn't find log file.")
            self.ui.logs.setText("Log file not found")

    def copy_clipboard(self):
        self.ui.logs.selectAll()
        self.ui.logs.copy()


def main():
    """Launch the window."""
    window = MyForm()
    window.exec()


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function
