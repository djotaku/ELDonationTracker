"""Launch the command line version of the program."""

import signal
import sys
import time

import eldonationtracker.api.participant as participant
import eldonationtracker.utils.extralife_io as extralife_io


def exit_triggered(a_signal, frame):
    print("\nExiting...")
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_triggered)
    participant_conf = extralife_io.ParticipantConf()
    my_participant = participant.Participant(participant_conf)
    while True:
        my_participant.run()
        time.sleep(15)
