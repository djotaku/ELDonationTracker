# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QTdesignerfiles/tracker.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(985, 137)
        Dialog.setAutoFillBackground(False)
        Dialog.setStyleSheet("background: rgba(255, 255, 255, 0)\n"
"")
        self.graphicsView = QtWidgets.QGraphicsView(Dialog)
        self.graphicsView.setEnabled(True)
        self.graphicsView.setGeometry(QtCore.QRect(0, -10, 991, 151))
        self.graphicsView.setAutoFillBackground(False)
        self.graphicsView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.graphicsView.setLineWidth(0)
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.graphicsView.setBackgroundBrush(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.graphicsView.setForegroundBrush(brush)
        self.graphicsView.setInteractive(False)
        self.graphicsView.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.graphicsView.setObjectName("graphicsView")
        self.Donation_label = QtWidgets.QTextEdit(Dialog)
        self.Donation_label.setGeometry(QtCore.QRect(180, 0, 801, 131))
        font = QtGui.QFont()
        font.setPointSize(56)
        self.Donation_label.setFont(font)
        self.Donation_label.setAutoFillBackground(False)
        self.Donation_label.setStyleSheet("background: rgba(255, 255, 255, 0)\n"
"")
        self.Donation_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Donation_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Donation_label.setLineWidth(0)
        self.Donation_label.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.Donation_label.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.Donation_label.setUndoRedoEnabled(False)
        self.Donation_label.setReadOnly(True)
        self.Donation_label.setObjectName("Donation_label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Tracker"))
        self.Donation_label.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Liberation Sans\'; font-size:56pt; font-weight:400; font-style:normal;\" bgcolor=\"transparent\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Liberation Sans\';\"><br /></p></body></html>"))
