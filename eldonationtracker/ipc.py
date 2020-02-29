"""Writes to an IPC value to allow different modules to pass information.

This is used to allow the tracker to know that new data needs to be read
in because a new donation has ocurred.
"""


def writeIPC(folder: str, value: str):
    """Write to the IPC file.

    This is used to let the call_tracker module know that a new\
    donation has been made.

    :param folder: The location of trackerIPC.txt
    :param value: The value to write to the file.
    :raises: IOError
    """
    folders = folder
    try:
        with open(f'{folders}/trackerIPC.txt', 'w') as file:
            file.write(value)
            file.close
    except IOError:
        print("""No trackerIPC.txt found.
            Have you updated the settings?
            Have you hit the 'run' button?""")
