description

# Installation/Usage Instructions

## tl;dr: 
**Windows Users**
Grab one of the 2 files below. You can choose :

- the single-binary (eldonationtracker.for.Windows.v5.2.4.exe): One file that you use to launch the program. 
- the zip file (Extra Life Donation Tracker for Windows v5.2.4.zip - which has been the main release method for at least a year now): A folder in which you'll find the executable.

The trade-off is that the single-binary is simpler, but takes a little longer to launch.

**Linux users**
use PyPi or git clone.

**Docker or Podman users***
docker run -it -v ./extralifedonationtracker:/root/.config/extralifedonationtracker -v ./testoutput:/root/output djotaku/eldonationtracker:5.3
or
podman run -it -v ./extralifedonationtracker:/root/.config/extralifedonationtracker:Z -v ./testoutput:/root/output:Z djotaku/eldonationtracker:5.3

## For more detailed instructions

Installation Instructions: https://eldonationtracker.readthedocs.io/en/latest/installation.html

Usage Instructions: https://eldonationtracker.readthedocs.io/en/latest/usage.html

Please file any bug reports. Pull requests welcome on the devel branch.