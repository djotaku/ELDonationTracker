"""Launch the command line version of the program."""

import signal
import sys
import time
import logging
from rich import print  # type ignore
from rich.logging import RichHandler  # type ignore

import eldonationtracker.api.participant as participant
import eldonationtracker.utils.extralife_io as extralife_io


def exit_triggered(a_signal, frame):
    print("[green]\nExiting...[/green]")
    sys.exit(0)


# logging
LOG_FORMAT = '%(name)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, handlers=[RichHandler(markup=True, show_path=False)])

if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_triggered)
    participant_conf = extralife_io.ParticipantConf()
    my_participant = participant.Participant(participant_conf)
    while True:
        my_participant.run()
        time.sleep(15)
