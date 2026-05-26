# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tracker.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
    Qt)
from PySide6.QtGui import (QBrush, QColor, QFont)
from PySide6.QtWidgets import (QFrame, QGraphicsView,
    QTextEdit)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(985, 137)
        Dialog.setAutoFillBackground(False)
        Dialog.setStyleSheet(u"background: rgba(255, 255, 255, 0)\n"
"")
        self.graphicsView = QGraphicsView(Dialog)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setEnabled(True)
        self.graphicsView.setGeometry(QRect(0, -10, 991, 151))
        self.graphicsView.setAutoFillBackground(False)
        self.graphicsView.setFrameShape(QFrame.NoFrame)
        self.graphicsView.setLineWidth(0)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        brush = QBrush(QColor(0, 170, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        self.graphicsView.setBackgroundBrush(brush)
        brush1 = QBrush(QColor(0, 0, 0, 255))
        brush1.setStyle(Qt.BrushStyle.NoBrush)
        self.graphicsView.setForegroundBrush(brush1)
        self.graphicsView.setInteractive(False)
        self.graphicsView.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.Donation_label = QTextEdit(Dialog)
        self.Donation_label.setObjectName(u"Donation_label")
        self.Donation_label.setGeometry(QRect(180, 0, 801, 131))
        font = QFont()
        font.setPointSize(56)
        self.Donation_label.setFont(font)
        self.Donation_label.setAutoFillBackground(False)
        self.Donation_label.setStyleSheet(u"background: rgba(255, 255, 255, 0)\n"
"")
        self.Donation_label.setFrameShape(QFrame.NoFrame)
        self.Donation_label.setFrameShadow(QFrame.Plain)
        self.Donation_label.setLineWidth(0)
        self.Donation_label.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Donation_label.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Donation_label.setUndoRedoEnabled(False)
        self.Donation_label.setReadOnly(True)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Tracker", None))
        self.Donation_label.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Liberation Sans'; font-size:56pt; font-weight:400; font-style:normal;\" bgcolor=\"transparent\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Liberation Sans';\"><br /></p></body></html>", None))
    # retranslateUi

