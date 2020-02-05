![Lint_Test](https://github.com/djotaku/ELDonationTracker/workflows/Lint_Test/badge.svg?branch=devel)

Would you like to be able to update your donations in real-time during a Live Stream or while recording a Let's Play as in the following screenshots?

![Updates while in-game](https://github.com/djotaku/ELDonationTracker/blob/devel/screenshots/IngameUpdates.png)

![Updates while the webcam is the main focus](https://github.com/djotaku/ELDonationTracker/blob/devel/screenshots/RecentDonations.png)

Read ahead to find out how!

If you find this useful, please consider donating to my Extra Life campagin: http://extralife.ericmesa.com -> I modify this link each year to point to my latest Extra Life campaign.

# How To use with a GUI

Watch one of these videos:

<a href="https://youtu.be/ruS6GUZiceQ" target="_blank">How to use Extra Life Donation Tracker with Linux</a>

<a href="https://youtu.be/yPL3hDivwPE" target="_blank">How to use Extra Life Donation Tracker with Wkndows</a>

or follow the instructions below:

NOTE: Major Changes occurred in the v3.0 release. Make sure to read the release notes!

I am now creating executables with each release. Download the executable that goes with your operating system. After you unzip or untar the file:

On Windows launch gui.exe.

On Linux launch gui - you may first need to chmod 775 to make it executable.

Then click on the Settings button to fill in the fields there. If you wish to have your settings persist across version updates, click on Persist Settings. Otherwise, click save and exit the settings window. Open the tracker window and capture that window in OBS or XSplit. In the main GUI hit Run to grab your data for the first time. From there, use the text files it generates in OBS or XSplit.

# How To use without a GUI

NOTE: These videos are VERY OUT OF DATE. 

To watch a video of how to use this program on Linux: https://youtu.be/sKaFQPoQeJw

To watch a video of how to use this program on Windows: https://youtu.be/hN94aPcEFng 

Or follow the instructions below: 

## Setup
First you should edit the values in participant.conf

Note:

- The values to the right of the : should be in quotation marks.
- if you're not in a team, the TeamID should be set to 'null' without quotation marks.

## To run

On Linux you should type:

python3 extralifedonations.py

On Windows it's easiest to open extralifedonations.py in IDLE and then run the script from there. (This avoids any issues with python being in your path)

# How To for developers

Please see CONTRIBUTING.MD if you wish to contribute. 

If you prefer to run from a git clone or from downloading one of the source downloads, follow the instructions below:

## Linux

If you wish to work in a virtual environment (and leave your system's Python packages alone), then type:

python3 -m venv .

source ./bin/activate 

(when you're done, you can type deactivate)

to grab the requirements:

pip install -r requirements.txt

Finally, decide if you want the GUI or just the commandline. If commandline, only:

Fist edit the participant.conf file in a text editor. Then run:

python3 extralifedonations.py

for the GUI type:

python3 gui.py 

The benefit you get from using the GUI is that cnce the GUI comes up you can click "tracker" to get a window that will display an image and text when a donation is registered

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
