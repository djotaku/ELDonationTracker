# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTextBrowser, QTextEdit,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(789, 778)
        icon = QIcon()
        icon.addFile(u"icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionDocumentation = QAction(MainWindow)
        self.actionDocumentation.setObjectName(u"actionDocumentation")
        self.actionCheck_for_Update = QAction(MainWindow)
        self.actionCheck_for_Update.setObjectName(u"actionCheck_for_Update")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionShow_Logs = QAction(MainWindow)
        self.actionShow_Logs.setObjectName(u"actionShow_Logs")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.ParticipantInfo = QGroupBox(self.centralwidget)
        self.ParticipantInfo.setObjectName(u"ParticipantInfo")
        self.ParticipantInfo.setGeometry(QRect(10, 60, 301, 301))
        self.gridLayoutWidget_2 = QWidget(self.ParticipantInfo)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(10, 20, 281, 295))
        self.gridLayout = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_total_num_donations = QLabel(self.gridLayoutWidget_2)
        self.label_total_num_donations.setObjectName(u"label_total_num_donations")
        self.label_total_num_donations.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_total_num_donations, 1, 1, 1, 1)

        self.AvgDonation = QTextBrowser(self.gridLayoutWidget_2)
        self.AvgDonation.setObjectName(u"AvgDonation")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.AvgDonation.sizePolicy().hasHeightForWidth())
        self.AvgDonation.setSizePolicy(sizePolicy1)
        self.AvgDonation.setMaximumSize(QSize(100, 50))
        self.AvgDonation.setFrameShape(QFrame.NoFrame)

        self.gridLayout.addWidget(self.AvgDonation, 4, 1, 1, 1)

        self.TotalRaised = QTextBrowser(self.gridLayoutWidget_2)
        self.TotalRaised.setObjectName(u"TotalRaised")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.TotalRaised.sizePolicy().hasHeightForWidth())
        self.TotalRaised.setSizePolicy(sizePolicy2)
        self.TotalRaised.setMaximumSize(QSize(100, 50))
        self.TotalRaised.setFrameShape(QFrame.NoFrame)

        self.gridLayout.addWidget(self.TotalRaised, 4, 0, 1, 1)

        self.label_avg_donations = QLabel(self.gridLayoutWidget_2)
        self.label_avg_donations.setObjectName(u"label_avg_donations")
        self.label_avg_donations.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_avg_donations, 3, 1, 1, 1)

        self.Goal = QTextBrowser(self.gridLayoutWidget_2)
        self.Goal.setObjectName(u"Goal")
        sizePolicy2.setHeightForWidth(self.Goal.sizePolicy().hasHeightForWidth())
        self.Goal.setSizePolicy(sizePolicy2)
        self.Goal.setMaximumSize(QSize(100, 50))
        self.Goal.setBaseSize(QSize(0, 0))
        self.Goal.setFrameShape(QFrame.NoFrame)
        self.Goal.setFrameShadow(QFrame.Plain)

        self.gridLayout.addWidget(self.Goal, 2, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 115, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_2, 0, 1, 1, 1)

        self.label_goal = QLabel(self.gridLayoutWidget_2)
        self.label_goal.setObjectName(u"label_goal")
        self.label_goal.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_goal, 1, 0, 1, 1)

        self.label_totalraised = QLabel(self.gridLayoutWidget_2)
        self.label_totalraised.setObjectName(u"label_totalraised")
        self.label_totalraised.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_totalraised, 3, 0, 1, 1)

        self.TotalNumDonations = QTextBrowser(self.gridLayoutWidget_2)
        self.TotalNumDonations.setObjectName(u"TotalNumDonations")
        sizePolicy1.setHeightForWidth(self.TotalNumDonations.sizePolicy().hasHeightForWidth())
        self.TotalNumDonations.setSizePolicy(sizePolicy1)
        self.TotalNumDonations.setMaximumSize(QSize(100, 50))
        self.TotalNumDonations.setFrameShape(QFrame.NoFrame)

        self.gridLayout.addWidget(self.TotalNumDonations, 2, 1, 1, 1)

        self.DonationInfo = QGroupBox(self.centralwidget)
        self.DonationInfo.setObjectName(u"DonationInfo")
        self.DonationInfo.setGeometry(QRect(330, 60, 451, 301))
        self.label = QLabel(self.DonationInfo)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 140, 121, 16))
        self.RecentDonations = QTextBrowser(self.DonationInfo)
        self.RecentDonations.setObjectName(u"RecentDonations")
        self.RecentDonations.setGeometry(QRect(10, 160, 431, 101))
        self.RecentDonations.setAutoFillBackground(False)
        self.RecentDonations.setLineWrapMode(QTextEdit.NoWrap)
        self.LastDonation = QTextBrowser(self.DonationInfo)
        self.LastDonation.setObjectName(u"LastDonation")
        self.LastDonation.setGeometry(QRect(10, 40, 431, 31))
        self.LastDonation.setAutoFillBackground(False)
        self.LastDonation.setFrameShape(QFrame.NoFrame)
        self.LastDonation.setFrameShadow(QFrame.Plain)
        self.label_2 = QLabel(self.DonationInfo)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 20, 81, 16))
        self.label_3 = QLabel(self.DonationInfo)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 80, 81, 16))
        self.TopDonation = QTextBrowser(self.DonationInfo)
        self.TopDonation.setObjectName(u"TopDonation")
        self.TopDonation.setGeometry(QRect(10, 100, 431, 31))
        self.TopDonation.setFrameShape(QFrame.NoFrame)
        self.TeamGroupBox = QGroupBox(self.centralwidget)
        self.TeamGroupBox.setObjectName(u"TeamGroupBox")
        self.TeamGroupBox.setGeometry(QRect(10, 370, 771, 291))
        self.gridLayoutWidget = QWidget(self.TeamGroupBox)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 30, 751, 251))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_2 = QSpacerItem(62, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.label_TeamTotalRaised = QLabel(self.gridLayoutWidget)
        self.label_TeamTotalRaised.setObjectName(u"label_TeamTotalRaised")
        self.label_TeamTotalRaised.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.gridLayout_2.addWidget(self.label_TeamTotalRaised, 1, 4, 1, 1)

        self.textBrowser_TeamTop5 = QTextBrowser(self.gridLayoutWidget)
        self.textBrowser_TeamTop5.setObjectName(u"textBrowser_TeamTop5")

        self.gridLayout_2.addWidget(self.textBrowser_TeamTop5, 3, 2, 1, 4)

        self.label_TeamGoal = QLabel(self.gridLayoutWidget)
        self.label_TeamGoal.setObjectName(u"label_TeamGoal")
        self.label_TeamGoal.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.gridLayout_2.addWidget(self.label_TeamGoal, 1, 2, 1, 1)

        self.label_11 = QLabel(self.gridLayoutWidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.gridLayout_2.addWidget(self.label_11, 0, 5, 1, 1)

        self.label_10 = QLabel(self.gridLayoutWidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.gridLayout_2.addWidget(self.label_10, 0, 2, 1, 1)

        self.label_TeamNumDonations = QLabel(self.gridLayoutWidget)
        self.label_TeamNumDonations.setObjectName(u"label_TeamNumDonations")
        self.label_TeamNumDonations.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.gridLayout_2.addWidget(self.label_TeamNumDonations, 1, 5, 1, 1)

        self.label_12 = QLabel(self.gridLayoutWidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.gridLayout_2.addWidget(self.label_12, 0, 4, 1, 1)

        self.label_13 = QLabel(self.gridLayoutWidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.gridLayout_2.addWidget(self.label_13, 2, 6, 1, 1)

        self.horizontalSpacer = QSpacerItem(254, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 6, 1, 1)

        self.label_TeamCaptain = QLabel(self.gridLayoutWidget)
        self.label_TeamCaptain.setObjectName(u"label_TeamCaptain")
        self.label_TeamCaptain.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.gridLayout_2.addWidget(self.label_TeamCaptain, 1, 1, 1, 1)

        self.label_14 = QLabel(self.gridLayoutWidget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.gridLayout_2.addWidget(self.label_14, 2, 4, 1, 1)

        self.label_9 = QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.gridLayout_2.addWidget(self.label_9, 0, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer, 2, 1, 1, 1)

        self.label_TopTeamParticipant = QLabel(self.gridLayoutWidget)
        self.label_TopTeamParticipant.setObjectName(u"label_TopTeamParticipant")
        self.label_TopTeamParticipant.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.gridLayout_2.addWidget(self.label_TopTeamParticipant, 3, 6, 1, 1)

        self.pushButtonRun = QPushButton(self.centralwidget)
        self.pushButtonRun.setObjectName(u"pushButtonRun")
        self.pushButtonRun.setGeometry(QRect(570, 670, 84, 31))
        self.pushButtonStop = QPushButton(self.centralwidget)
        self.pushButtonStop.setObjectName(u"pushButtonStop")
        self.pushButtonStop.setGeometry(QRect(670, 670, 84, 31))
        self.CopyrightLabel = QLabel(self.centralwidget)
        self.CopyrightLabel.setObjectName(u"CopyrightLabel")
        self.CopyrightLabel.setGeometry(QRect(30, 680, 481, 31))
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 771, 33))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.SettingsButton = QPushButton(self.layoutWidget)
        self.SettingsButton.setObjectName(u"SettingsButton")
        self.SettingsButton.setAutoDefault(False)
        self.SettingsButton.setFlat(False)

        self.horizontalLayout.addWidget(self.SettingsButton)

        self.TrackerButton = QPushButton(self.layoutWidget)
        self.TrackerButton.setObjectName(u"TrackerButton")

        self.horizontalLayout.addWidget(self.TrackerButton)

        self.ProgressBarButton = QPushButton(self.layoutWidget)
        self.ProgressBarButton.setObjectName(u"ProgressBarButton")

        self.horizontalLayout.addWidget(self.ProgressBarButton)

        self.RefreshButton = QPushButton(self.layoutWidget)
        self.RefreshButton.setObjectName(u"RefreshButton")

        self.horizontalLayout.addWidget(self.RefreshButton)

        self.TestAlertButton = QPushButton(self.layoutWidget)
        self.TestAlertButton.setObjectName(u"TestAlertButton")

        self.horizontalLayout.addWidget(self.TestAlertButton)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 789, 32))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menuBar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionShow_Logs)
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addAction(self.actionCheck_for_Update)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        self.SettingsButton.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"EL Donation Tracker", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"&Quit", None))
        self.actionDocumentation.setText(QCoreApplication.translate("MainWindow", u"&Documentation", None))
#if QT_CONFIG(tooltip)
        self.actionDocumentation.setToolTip(QCoreApplication.translate("MainWindow", u"Open Documentation in your default browser", None))
#endif // QT_CONFIG(tooltip)
        self.actionCheck_for_Update.setText(QCoreApplication.translate("MainWindow", u"&Check for Update", None))
#if QT_CONFIG(tooltip)
        self.actionCheck_for_Update.setToolTip(QCoreApplication.translate("MainWindow", u"Checks for Updates", None))
#endif // QT_CONFIG(tooltip)
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"&About ELDonationTracker", None))
        self.actionShow_Logs.setText(QCoreApplication.translate("MainWindow", u"&Show Logs", None))
        self.ParticipantInfo.setTitle(QCoreApplication.translate("MainWindow", u"Participant Info", None))
        self.label_total_num_donations.setText(QCoreApplication.translate("MainWindow", u"Total # of Donations", None))
        self.label_avg_donations.setText(QCoreApplication.translate("MainWindow", u"Average Donation", None))
        self.label_goal.setText(QCoreApplication.translate("MainWindow", u"Goal", None))
        self.label_totalraised.setText(QCoreApplication.translate("MainWindow", u"Total Raised", None))
        self.DonationInfo.setTitle(QCoreApplication.translate("MainWindow", u"Participant Donation Info", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Recent Donations", None))
        self.RecentDonations.setDocumentTitle("")
        self.RecentDonations.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Recent Donations", None))
        self.LastDonation.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Last Donation", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Last Donation", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Top Donor", None))
        self.TopDonation.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Top Donor", None))
        self.TeamGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Team Info", None))
        self.label_TeamTotalRaised.setText(QCoreApplication.translate("MainWindow", u"Raised", None))
        self.label_TeamGoal.setText(QCoreApplication.translate("MainWindow", u"Team Goal", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"# of Donations", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Goal", None))
        self.label_TeamNumDonations.setText(QCoreApplication.translate("MainWindow", u"# Donations", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Total Raised", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Top Team Participant", None))
        self.label_TeamCaptain.setText(QCoreApplication.translate("MainWindow", u"Team Captain", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Top 5 Team Participants", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Team Captain", None))
        self.label_TopTeamParticipant.setText(QCoreApplication.translate("MainWindow", u"Top Team Participant", None))
        self.pushButtonRun.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.pushButtonStop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.CopyrightLabel.setText(QCoreApplication.translate("MainWindow", u"\u00a9 2015-2024 Eric Mesa; Licensed GPLv3; http://extralife.ericmesa.com", None))
#if QT_CONFIG(tooltip)
        self.SettingsButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Change folders, Extra Life ID, etc</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.SettingsButton.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.TrackerButton.setText(QCoreApplication.translate("MainWindow", u"Tracker", None))
        self.ProgressBarButton.setText(QCoreApplication.translate("MainWindow", u"Progress Bar", None))
        self.RefreshButton.setText(QCoreApplication.translate("MainWindow", u"Force Refresh", None))
        self.TestAlertButton.setText(QCoreApplication.translate("MainWindow", u"Test Alert", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"Fi&le", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

