import json, unicodedata

def loadJSON():
    with open('participant.conf') as file:
        return json.load(file)

def CLIvalues():
    participantconf = loadJSON()
    return (participantconf['ExtraLifeID'],participantconf['textFolder'], participantconf['CurrencySymbol'], participantconf['TeamID'])

def textfolderOnly():
    participantconf = loadJSON()
    return participantconf['textFolder']
