# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tracker.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(985, 137)
        Dialog.setAutoFillBackground(False)
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
        self.Donation_label = QtWidgets.QLabel(Dialog)
        self.Donation_label.setGeometry(QtCore.QRect(170, 0, 811, 121))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(101, 104, 106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.Donation_label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(43)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.Donation_label.setFont(font)
        self.Donation_label.setText("")
        self.Donation_label.setTextFormat(QtCore.Qt.PlainText)
        self.Donation_label.setScaledContents(False)
        self.Donation_label.setWordWrap(True)
        self.Donation_label.setObjectName("Donation_label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Tracker"))

