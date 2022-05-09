![Lint,PyTest, MyPy, and Coverage](https://github.com/djotaku/ELDonationTracker/workflows/Lint,PyTest,%20MyPy,%20and%20Coverage/badge.svg?branch=master) ![Windows Build](https://github.com/djotaku/ELDonationTracker/workflows/Windows%20Build/badge.svg) [![Documentation Status](https://readthedocs.org/projects/eldonationtracker/badge/?version=latest)](https://eldonationtracker.readthedocs.io/en/latest/?badge=latest) ![Upload Python Package](https://github.com/djotaku/ELDonationTracker/workflows/Upload%20Python%20Package/badge.svg) [![codecov](https://codecov.io/gh/djotaku/ELDonationTracker/branch/master/graph/badge.svg)](https://codecov.io/gh/djotaku/ELDonationTracker)



Would you like to be able to update your donations in real-time during a Live Stream or while recording a Let's Play as in the animated gif below?

![OBSwithExtraLifeRunning](https://github.com/djotaku/ELDonationTracker/blob/5082d36148aa0a9ed850b179ae858d0aa3db8cb4/screenshots/OBS.GIF)


Read ahead to find out how!

If you find this useful, please consider donating to my [Extra Life campagin](http://extralife.ericmesa.com)

# How To for Users

visit: http://djotaku.github.io/ELDonationTracker/ for video instructions on how to use the program.

If you prefer text instructions, read the documentation at: https://eldonationtracker.readthedocs.io/en/latest/index.html

The quickstart instructions are:
- Go to releases and the most recent release
- If you're on Windows:
  - grab the file at the bottom
  - launch it
  - Click on the config button to fill out the config
  - Hit run and it will populate the folder you picked in config with the data you can use in OBS/XSplit for your overlay
- If you're on Linux:
  - You can use PyPi to install eldonationtracker
  - You can git clone this repo, install the requirements and go from there
  - If you need the GUI you can use Docker or Podman with a command that looks like:
  ```bash
  docker run -it -v ./extralifedonationtracker:/root/.config/extralifedonationtracker -v ./testoutput:/root/output djotaku/eldonationtracker:latest

  # or

   podman run -it -v ./extralifedonationtracker:/root/.config/extralifedonationtracker:Z -v ./testoutput:/root/output:Z djotaku/eldonationtracker:latest
  ```

# How To for developers

Please see [CONTRIBUTING.MD](https://github.com/djotaku/ELDonationTracker/blob/master/CONTRIBUTING.md) if you wish to contribute.

Modules are well-documented at: https://eldonationtracker.readthedocs.io/en/latest/py-modindex.html

# Support

If anything goes wrong, please open a Bug Report under issues.

If you want a new type of output data, fill out a Reequest for New Output Data issue

If there's documentation missing, fill out the Missing Documentation issue
