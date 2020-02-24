Development branch badges:![Lint_Test](https://github.com/djotaku/ELDonationTracker/workflows/Lint_Test/badge.svg?branch=devel)

Master branch badges:![Lint_Test](https://github.com/djotaku/ELDonationTracker/workflows/Lint_Test/badge.svg) ![Linux_Build](https://github.com/djotaku/ELDonationTracker/workflows/Linux_Build/badge.svg) ![Windows_Build](https://github.com/djotaku/ELDonationTracker/workflows/Windows_Build/badge.svg)

[![Documentation Status](https://readthedocs.org/projects/eldonationtracker/badge/?version=latest)](https://eldonationtracker.readthedocs.io/en/latest/?badge=latest)

Would you like to be able to update your donations in real-time during a Live Stream or while recording a Let's Play as in the following screenshots?

![Updates while in-game](https://github.com/djotaku/ELDonationTracker/raw/devel/screenshots/IngameUpdates.png)

Read ahead to find out how!

If you find this useful, please consider donating to my [Extra Life campagin](http://extralife.ericmesa.com)

# Users

visit: http://djotaku.github.io/ELDonationTracker/ for instructions on how to use the program.

If you prefer text instructions, read the documentation at: https://eldonationtracker.readthedocs.io/en/latest/index.html

# How To for developers

Please see [CONTRIBUTING.MD](https://github.com/djotaku/ELDonationTracker/blob/master/CONTRIBUTING.md) if you wish to contribute. 

Modules are well-documented at: https://eldonationtracker.readthedocs.io/en/latest/py-modindex.html


# Web GUI - currently unmaintained

If you want a webpage you can use as a GUI to do a sanity check on what should be in the donation files, first change the folder at the end in the __main__ section (this should be the same folder you're using for the text files). Then run

python createHTML.py 

Then open mainpage.html at the folder you told it to use. It should update every 15 seconds.

(Currently web page creation is still python 2)

tracker.html part still needs a little work.

# Support

If you want support for other configurations, please open an issue.
