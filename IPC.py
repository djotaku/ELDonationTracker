"""Writes to an IPC value to allow different modules to pass information.

This is used to allow the tracker to know that new data needs to be read
in because a new donation has ocurred.
"""

import sys
import readparticipantconf


def writeIPC(value):
    """Write to the IPC file."""
    folders = readparticipantconf.textfolderOnly()
    f = open(f'{folders}/trackerIPC.txt', 'w')
    f.write(value)
    f.close
