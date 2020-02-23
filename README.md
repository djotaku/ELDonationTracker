Development branch badges:![Lint_Test](https://github.com/djotaku/ELDonationTracker/workflows/Lint_Test/badge.svg?branch=devel)

Master branch badges:![Lint_Test](https://github.com/djotaku/ELDonationTracker/workflows/Lint_Test/badge.svg) ![Linux_Build](https://github.com/djotaku/ELDonationTracker/workflows/Linux_Build/badge.svg) ![Windows_Build](https://github.com/djotaku/ELDonationTracker/workflows/Windows_Build/badge.svg)

[![Documentation Status](https://readthedocs.org/projects/eldonationtracker/badge/?version=latest)](https://eldonationtracker.readthedocs.io/en/latest/?badge=latest)

Would you like to be able to update your donations in real-time during a Live Stream or while recording a Let's Play as in the following screenshots?

![Updates while in-game](https://github.com/djotaku/ELDonationTracker/raw/devel/screenshots/IngameUpdates.png)

Read ahead to find out how!

If you find this useful, please consider donating to my [Extra Life campagin](http://extralife.ericmesa.com)

For users, visit: http://djotaku.github.io/ELDonationTracker/ for instructions.

# How To for developers

Please see [CONTRIBUTING.MD](https://github.com/djotaku/ELDonationTracker/blob/master/CONTRIBUTING.md) if you wish to contribute. 

If you prefer to run from a git clone or from downloading one of the source downloads, follow the instructions below:

## Linux

If you wish to work in a virtual environment (and leave your system's Python packages alone), then type:

python3 -m venv .

source ./bin/activate 

(when you're done, you can type deactivate)

to grab the requirements:

pip install -r requirements.txt

Finally, decide if you want to use the GUI or just the commandline. If commandline, only:

Fist edit the participant.conf file in a text editor. Then run:

python3 extralifedonations.py

for the GUI type:

python3 gui.py 

The benefit you get from using the GUI is that once the GUI comes up you can click "tracker" to get a window that will display an image and text when a donation is registered

Use the settings window to enter your settings and then hit save to save them. 

To run the program, hit run. You should get the same output on the commandline as when just running the commandline utility. 

## Windows

You will need the PyQt5 packages. If you already have Python installed from the official Python release (see the video above if you need help), then go to the directory with the files you downloaded from Github and type:

python -m pip install -r rquirements.txt 

If you're using Windows Explorer - double-click on gui.py. If you're on the Windows commandline you should be able to type python gui.py. 

Once the GUI comes up you can click "tracker" to get a window that will display an image and text when a donation is registered

Use the settings window to enter your settings and then hit save to save them. 

To run the program, hit run. You should get the same output on the commandline as when just running the commandline utility. 

# Web GUI - currently unmaintained

If you want a webpage you can use as a GUI to do a sanity check on what should be in the donation files, first change the folder at the end in the __main__ section (this should be the same folder you're using for the text files). Then run

python createHTML.py 

Then open mainpage.html at the folder you told it to use. It should update every 15 seconds.

(Currently web page creation is still python 2)

tracker.html part still needs a little work.

# Support

If you want support for other configurations, please open an issue.
