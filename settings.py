# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(612, 279)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 40, 91, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 90, 71, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(40, 140, 101, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(60, 190, 56, 15))
        self.label_4.setObjectName("label_4")
        self.lineEditParticipantID = QtWidgets.QLineEdit(Dialog)
        self.lineEditParticipantID.setGeometry(QtCore.QRect(150, 30, 113, 29))
        self.lineEditParticipantID.setObjectName("lineEditParticipantID")
        self.lineEditCurrencySymbol = QtWidgets.QLineEdit(Dialog)
        self.lineEditCurrencySymbol.setGeometry(QtCore.QRect(170, 130, 113, 29))
        self.lineEditCurrencySymbol.setObjectName("lineEditCurrencySymbol")
        self.lineEditTeamID = QtWidgets.QLineEdit(Dialog)
        self.lineEditTeamID.setGeometry(QtCore.QRect(160, 180, 113, 29))
        self.lineEditTeamID.setObjectName("lineEditTeamID")
        self.pushButtonSelectFolder = QtWidgets.QPushButton(Dialog)
        self.pushButtonSelectFolder.setGeometry(QtCore.QRect(450, 80, 84, 31))
        self.pushButtonSelectFolder.setObjectName("pushButtonSelectFolder")
        self.labelTextFolder = QtWidgets.QLabel(Dialog)
        self.labelTextFolder.setGeometry(QtCore.QRect(160, 90, 271, 16))
        self.labelTextFolder.setObjectName("labelTextFolder")
        self.pushButtonRevert = QtWidgets.QPushButton(Dialog)
        self.pushButtonRevert.setGeometry(QtCore.QRect(410, 240, 84, 31))
        self.pushButtonRevert.setObjectName("pushButtonRevert")
        self.pushButtonSave = QtWidgets.QPushButton(Dialog)
        self.pushButtonSave.setGeometry(QtCore.QRect(510, 240, 84, 31))
        self.pushButtonSave.setObjectName("pushButtonSave")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))
        self.label.setText(_translate("Dialog", "Participant ID"))
        self.label_2.setText(_translate("Dialog", "Text Folder"))
        self.label_3.setText(_translate("Dialog", "Currency Symbol"))
        self.label_4.setText(_translate("Dialog", "Team ID"))
        self.pushButtonSelectFolder.setText(_translate("Dialog", "select Folder"))
        self.labelTextFolder.setText(_translate("Dialog", "No Folder Selected"))
        self.pushButtonRevert.setText(_translate("Dialog", "Revert"))
        self.pushButtonSave.setText(_translate("Dialog", "Save"))

