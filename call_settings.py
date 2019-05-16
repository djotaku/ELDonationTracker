import sys
import json
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from settings import *

class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        with open('participant.conf') as file:
            self.participantconf = json.load(file)
        (self.ExtraLifeID,self.textFolder,self.CurrencySymbol, self.TeamID) = (self.participantconf['ExtraLifeID'],self.participantconf['textFolder'], self.participantconf['CurrencySymbol'], self.participantconf['TeamID'])
        self.ui.lineEditParticipantID.setText(self.ExtraLifeID)
        self.ui.labelTextFolder.setText(self.textFolder)
        self.ui.lineEditCurrencySymbol.setText(self.CurrencySymbol)
        self.ui.lineEditTeamID.setText(self.TeamID)
        self.ui.pushButtonRevert.clicked.connect(self.revert)
        self.ui.pushButtonSave.clicked.connect(self.save)
        self.ui.pushButtonSelectFolder.clicked.connect(self.selectfolder)
        self.show()
        
    def revert(self):
        self.ui.lineEditParticipantID.setText(self.ExtraLifeID)
        self.ui.labelTextFolder.setText(self.textFolder)
        self.ui.lineEditCurrencySymbol.setText(self.CurrencySymbol)
        self.ui.lineEditTeamID.setText(self.TeamID)
        
    def save(self):
        participantID = self.ui.lineEditParticipantID.text()
        textfolder = self.ui.labelTextFolder.text()
        currencysymbol = self.ui.lineEditCurrencySymbol.text()
        if self.ui.lineEditTeamID.text() == "":
            teamID = None
        else:
            teamID = self.ui.lineEditTeamID.text()
        config= {'ExtraLifeID':participantID, 'textFolder':textfolder,'CurrencySymbol':currencysymbol,'TeamID':teamID}
        with open('participant.conf','w') as outfile:
            json.dump(config,outfile)
        
    def selectfolder(self):
        directory = QFileDialog.getExistingDirectory(self, "Get Folder")
        self.ui.labelTextFolder.setText(directory)

def main():
    w = MyForm()
    w.exec()
        

if __name__=="__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
