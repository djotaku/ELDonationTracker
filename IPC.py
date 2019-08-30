import sys, readparticipantconf

def writeIPC(value):
    folders = readparticipantconf.textfolderOnly()
    f = open(f'{folders}/trackerIPC.txt', 'w')
    f.write(value)
    f.close
             
