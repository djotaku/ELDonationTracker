# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'logs.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QPushButton, QSizePolicy, QTextBrowser,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(740, 777)
        self.copy = QPushButton(Form)
        self.copy.setObjectName(u"copy")
        self.copy.setGeometry(QRect(10, 10, 121, 31))
        self.logs = QTextBrowser(Form)
        self.logs.setObjectName(u"logs")
        self.logs.setGeometry(QRect(10, 50, 721, 721))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.copy.setText(QCoreApplication.translate("Form", u"Copy to Clipboard", None))
    # retranslateUi

