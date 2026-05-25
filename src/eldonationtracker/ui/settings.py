# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
    QSize, Qt)
from PySide6.QtGui import (QIcon)
from PySide6.QtWidgets import (QGridLayout, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QPushButton,
    QSpinBox, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(805, 392)
        icon = QIcon()
        icon.addFile(u"icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Dialog.setWindowIcon(icon)
        self.layoutWidget = QWidget(Dialog)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 0, 791, 381))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.layoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 6, 0, 1, 1)

        self.pushButtonSelectFolder = QPushButton(self.layoutWidget)
        self.pushButtonSelectFolder.setObjectName(u"pushButtonSelectFolder")

        self.gridLayout.addWidget(self.pushButtonSelectFolder, 1, 3, 1, 2)

        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEditTeamID = QLineEdit(self.layoutWidget)
        self.lineEditTeamID.setObjectName(u"lineEditTeamID")

        self.gridLayout.addWidget(self.lineEditTeamID, 3, 1, 1, 1)

        self.label_tracker_image = QLabel(self.layoutWidget)
        self.label_tracker_image.setObjectName(u"label_tracker_image")
        self.label_tracker_image.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_tracker_image, 5, 1, 1, 1)

        self.lineEditParticipantID = QLineEdit(self.layoutWidget)
        self.lineEditParticipantID.setObjectName(u"lineEditParticipantID")
        self.lineEditParticipantID.setToolTipDuration(5)

        self.gridLayout.addWidget(self.lineEditParticipantID, 0, 1, 1, 1)

        self.pushButton_persistentsave = QPushButton(self.layoutWidget)
        self.pushButton_persistentsave.setObjectName(u"pushButton_persistentsave")

        self.gridLayout.addWidget(self.pushButton_persistentsave, 11, 2, 1, 3)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_font = QPushButton(self.layoutWidget)
        self.pushButton_font.setObjectName(u"pushButton_font")

        self.horizontalLayout_2.addWidget(self.pushButton_font)

        self.pushButton_font_color = QPushButton(self.layoutWidget)
        self.pushButton_font_color.setObjectName(u"pushButton_font_color")

        self.horizontalLayout_2.addWidget(self.pushButton_font_color)


        self.gridLayout.addLayout(self.horizontalLayout_2, 8, 1, 1, 1)

        self.lineEditCurrencySymbol = QLineEdit(self.layoutWidget)
        self.lineEditCurrencySymbol.setObjectName(u"lineEditCurrencySymbol")

        self.gridLayout.addWidget(self.lineEditCurrencySymbol, 2, 1, 1, 1)

        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.labelTextFolder = QLabel(self.layoutWidget)
        self.labelTextFolder.setObjectName(u"labelTextFolder")
        self.labelTextFolder.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.labelTextFolder, 1, 1, 1, 2)

        self.pushButton_tracker_background = QPushButton(self.layoutWidget)
        self.pushButton_tracker_background.setObjectName(u"pushButton_tracker_background")

        self.gridLayout.addWidget(self.pushButton_tracker_background, 9, 1, 1, 1)

        self.label_sound = QLabel(self.layoutWidget)
        self.label_sound.setObjectName(u"label_sound")
        self.label_sound.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_sound, 6, 1, 1, 1)

        self.label_donors_to_display = QLabel(self.layoutWidget)
        self.label_donors_to_display.setObjectName(u"label_donors_to_display")

        self.gridLayout.addWidget(self.label_donors_to_display, 4, 0, 1, 1)

        self.spinBox_DonorsToDisplay = QSpinBox(self.layoutWidget)
        self.spinBox_DonorsToDisplay.setObjectName(u"spinBox_DonorsToDisplay")

        self.gridLayout.addWidget(self.spinBox_DonorsToDisplay, 4, 1, 1, 1)

        self.pushButton_tracker_image = QPushButton(self.layoutWidget)
        self.pushButton_tracker_image.setObjectName(u"pushButton_tracker_image")

        self.gridLayout.addWidget(self.pushButton_tracker_image, 5, 2, 1, 1)

        self.pushButton_sound = QPushButton(self.layoutWidget)
        self.pushButton_sound.setObjectName(u"pushButton_sound")

        self.gridLayout.addWidget(self.pushButton_sound, 6, 2, 1, 1)

        self.pushButton_grab_image = QPushButton(self.layoutWidget)
        self.pushButton_grab_image.setObjectName(u"pushButton_grab_image")

        self.gridLayout.addWidget(self.pushButton_grab_image, 5, 4, 1, 1)

        self.pushButton_grab_sound = QPushButton(self.layoutWidget)
        self.pushButton_grab_sound.setObjectName(u"pushButton_grab_sound")

        self.gridLayout.addWidget(self.pushButton_grab_sound, 6, 4, 1, 1)

        self.pushButton_validate_participant_id = QPushButton(self.layoutWidget)
        self.pushButton_validate_participant_id.setObjectName(u"pushButton_validate_participant_id")

        self.gridLayout.addWidget(self.pushButton_validate_participant_id, 0, 2, 1, 1)

        self.pushButton_validate_team_id = QPushButton(self.layoutWidget)
        self.pushButton_validate_team_id.setObjectName(u"pushButton_validate_team_id")

        self.gridLayout.addWidget(self.pushButton_validate_team_id, 3, 2, 1, 1)

        self.pushButtonRevert = QPushButton(self.layoutWidget)
        self.pushButtonRevert.setObjectName(u"pushButtonRevert")

        self.gridLayout.addWidget(self.pushButtonRevert, 10, 2, 1, 3)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Settings", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Donation Sound", None))
#if QT_CONFIG(tooltip)
        self.pushButtonSelectFolder.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.pushButtonSelectFolder.setText(QCoreApplication.translate("Dialog", u"select Folder", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Team ID", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Text Folder", None))
        self.label_tracker_image.setText(QCoreApplication.translate("Dialog", u"No Image Selected", None))
#if QT_CONFIG(tooltip)
        self.lineEditParticipantID.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.pushButton_persistentsave.setStatusTip(QCoreApplication.translate("Dialog", u"To have the settings persist across upgrades", None))
#endif // QT_CONFIG(statustip)
        self.pushButton_persistentsave.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Currency Symbol", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Tracker Image", None))
        self.pushButton_font.setText(QCoreApplication.translate("Dialog", u"Tracker Font", None))
        self.pushButton_font_color.setText(QCoreApplication.translate("Dialog", u"Tracker Font Color", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Participant ID", None))
        self.labelTextFolder.setText(QCoreApplication.translate("Dialog", u"No Folder Selected", None))
        self.pushButton_tracker_background.setText(QCoreApplication.translate("Dialog", u"Change Tracker Background Color", None))
        self.label_sound.setText(QCoreApplication.translate("Dialog", u"No Sound Selected", None))
        self.label_donors_to_display.setText(QCoreApplication.translate("Dialog", u"Donors to Display", None))
        self.pushButton_tracker_image.setText(QCoreApplication.translate("Dialog", u"select Image", None))
        self.pushButton_sound.setText(QCoreApplication.translate("Dialog", u"select Sound", None))
        self.pushButton_grab_image.setText(QCoreApplication.translate("Dialog", u"Grab from Github", None))
        self.pushButton_grab_sound.setText(QCoreApplication.translate("Dialog", u"Grab from Github", None))
        self.pushButton_validate_participant_id.setText(QCoreApplication.translate("Dialog", u"Validate Participant ID", None))
        self.pushButton_validate_team_id.setText(QCoreApplication.translate("Dialog", u"Validate Team ID", None))
        self.pushButtonRevert.setText(QCoreApplication.translate("Dialog", u"Revert", None))
    # retranslateUi

