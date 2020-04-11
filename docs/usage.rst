=====
Usage
=====

GUI Single Executable users (Windows Users)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This refers to you if you downloaded a file like Extra Life Donation Tracker for Windows v3.4.zip. You may wish to watch a video on how to use the GUI at http://djotaku.github.io/ELDonationTracker/ . But if you prefer to read, continue below.

Launching
---------

Go into the folder you unzipped. Find the file called gui.exe and double-click it. If Windows or your anti-virus software throws a warning, click through to allow it to run.

.. note::

    In a future version, this may change to just be one executable instead of a folder full of files.

.. _gui-usage:

Using
-----

When you launch the GUI, it will look like this (colors will vary by your OS's color scheme):

.. image :: /images/GUI_startup.png

If this is not the first time you've used the GUI, it will eventually populate with data (I'll show that at the end). If you've never launched the GUI before and you haven't updated the :doc:`participant_conf` during a CLI run, the GUI won't know where to get the data or where to put it once it grabs it from the CLI. So the first thing you want to do is click on the settings window:

.. image :: /images/Settings_Window.png

The first thing to do here is to enter your participant ID. Where do you find that? Well, it's at the end of your extralife website URL. For example, for 2020, the URL to donate to my campaign is:

https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=401280

As you can see, right at the end it says "participantID=401280". If you look back at that settings window image, you'll see that's what I have in there. If you want to check that you've typed or copied the participant ID correctly, you can click on :guilabel:`Validate Participant ID` and it will attempt to connect to that API endpoint for that participant ID. If it is successful, you have the right participant ID (or coincidentally mistyped someone else's). If it's unsuccessful, the most likely reason is that you mistyped it, but you would also get that outcome if the API is unavailable.

.. versionadded:: 4.3.0
    Validate Participant ID

 - The next thing to change is the text folder. This is where eldonationtracker will create text files that you will use as inputs in OBS or XSplit. Every time something changes - you get a donation or the team (if you're part of one) gets a donation, those text files will change (as long as eldonationtracker is running) and so they'll change in real time on your screen in OBS or XSplit.

 - Now let's edit the Team ID. If you don't have a team, just make this blank. (No spaces!) Otherwise find your Team ID in a similar way as you found your participant ID. Go to your team page and the ID will be at the end of that URL. If you want to check that you've typed or copied the team ID correctly, you can click on :guilabel:`Validate Team ID` and it will attempt to connect to that API endpoint for that team ID. If it is successful, you have the right team ID (or coincidentally mistyped someone else's). If it's unsuccessful, the most likely reason is that you mistyped it, but you would also get that outcome if the API is unavailable.

.. versionadded:: 4.3.0
    Validate Team ID

 - Edit the Donors to Display field. Some of the text files produced by eldonationtracker (lastNDonations, topNdonors, etc) use this number to determine how many donors or donations to write to the file. I usually put it at about five, but I also don't get a lot of donations most years.

The final settings all deal with the tracker window. If you scroll just a little lower in this tutorial you'll see a rectangle with a green background and an image and some text appearing and disappearing. That window is what will appear on your screen when someone donates if you've properly set up OBS or XSplit to capture those windows.

 - You should select an image with a transparent background (most likely a gif or png) that will appear when someone donates. I'll show what it'll look like in a minute. If you would like to use the default image, click on :guilabel:`Grab from Github` next to the :guilabel:`select Image` button and it will grab it from GitHub and place it in the XDG location for your system. Make sure to hit :guilabel:`Persist Settings` afterward to save it to your settings.

.. versionadded:: 4.3.0
    The ability to grab the default image from GitHub.

 - Also select an MP3 file you would like to play when you get a donation. Keep it shorter than 15 seconds. If you would like to use the default mp3 (my daughter saying "you got a donation!"), click on :guilabel:`Grab from Github` next to the :guilabel:`select Sound` button and it will grab it from GitHub and place it in the XDG location for your system. Make sure to hit :guilabel:`Persist Settings` afterward to save it to your settings.

.. versionadded:: 4.3.0
    The ability to grab the default sound from GitHub.

 - With the last 3 buttons you can change the Font type and size, the font color, and the background color. I recommend a size around 48-50 (you may need to type it in yourself if it's not a selectable number). For the background color, it's probably best to stick with the chromakey green I've selected because that makes it incredibly easy for OBS or XSplit to make the background disappear so that on your screen you just see the image and text (not the green background). But if the image you want to use has a lot of green in it, you may need to choose bluescreen blue or some other color that will also work well with OBS or XSplit's chromakey filters.

.. versionadded:: 4.2.0
    Ability to change the font type, size, and color as well as the tracker background color.

.. warning::

    Because of the way QT color chooser dialogue windows work, if you pick a color and hit cancel, it will still change the color in the Tracker window. (whereas you have to click "ok" in the Font chooser window to change the font) If you go back in and pick one of the colors from the palette on the left, you can get it working again. Or you can life the right-most slider from black to white. Finally, if you can't remember what color you had quitting out of everything without saving should bring back the last color you saved (or the default).


- Finally, it's time to save your settings. The BEST option is to pick :guilabel:`Persist Settings`. Then it will save to a special location on your computer so that even as you upgrade (either grab new zip files from Github or update via PyPi or git pull) you won't have to keep inputting your settings. If you know for sure it's what you want to do, you can hit :guilabel:`Save` and it'll save in the folder where you're running the program. It *should* work on Windows and may or may not be there next time you launch on Linux. If you have not hit save or Persist Settings yet, Revert will reload whatever configuration information was in the file when you hit the Settings button.

OK, now it's time to test that things are working with your settings. Close the settings window and click on :guilabel:`Tracker`. Then hit test alert. If everything was correctly set up in the settings, you should see something like:

.. image :: /images/tracker.gif

And hear the sound you picked. What the text says will depend on whether you've ever run this program before either in GUI or on the commandline. If you've never run it, you'll get a test message. If you have run it and the settings are correctly configured, it should show whatever in your file called :file:`LastDonationNameAmnt.txt`.

OK, now it's time to hit :guilabel:`Run` and hopefully if all the directions have been followed and I haven't introduced any bugs, it should start grabbing data from the API. You should look at the commandline window for information. Whether you launched the GUI from gui.exe, used PyPi, or python gui, you should have a commandline window showing messages related to what's going on. It should look something roughly like this:

.. code-block:: Bash

    Looking for persistent settings at (this path will depend on your system)
    Persistent settings found.
    Participant.conf version check!
    Version is correct
    run button
    Starting Thread-1. But first, reloading config file.
    Looking for persistent settings at (this path will depend on your system)
    Persistent settings found.
    19:19:10

When you're done, be sure to hit stop. When you exit out, it will take a few seconds until it's done before the GUI will disappear. If you Go :menuselection:`File --> Quit`, that will also trigger it to stop. Again, it'll take a few seconds before it's all cleaned up and ready to disappear from your screen.
    
Finally, let's quickly go over the help menu items at the top of the GUI.

.. image :: /images/GUI_helpmenu.png


- :guilabel:`Documentation` will take you to the latest version of this very documentation you're reading now
- :guilabel:`Check for Update` will check if you have the latest version. It will then pop up a window to let you know.
- :guilabel:`About ELDonationTracker` will bring up a window with some URLs and copyright data. Eventually if we start getting more contributors, those would be listed there, too.
    
Commandline users (PyPi)
^^^^^^^^^^^^^^^^^^^^^^^^

Go to the folder you created in :doc:`installation`. If you don't have the virtual environment activated, start with that:

.. code-block:: Bash

    python3 -m venv .
    source ./bin/activate
    # to check for upgrades
    pip install --upgrade eldonationtracker


GUI
---

Make sure you have the :doc:`participant_conf` in the persistent location. You can grab the one in the GitHub repo or create your own by looking at the example there. Once the GUI has actually started, you can easily modify the config file via the GUI. To start the GUI:

.. code-block:: Bash

   python -m eldonationtracker.gui
   
That should work just fine. Keep an eye on the commandline for any errors or messages from eldonationtracker. The benefit you get from using the GUI is that once the GUI comes up you can click "tracker" to get a window that will display an image and text when a donation is registered. For text instructions on how to use the GUI, go to :ref:`gui-usage` or watch the video at http://djotaku.github.io/ELDonationTracker/

eg:

.. image :: /images/tracker.gif

You can also edit the settings in a GUI rather than on the commandline and those settings will persist to commandline-only usage..

Commandline Only (No GUI)
-------------------------

Make sure you have the :doc:`participant_conf` in the persistent location. You can grab the one in the Github repo or create your own by looking at the example there. To start the commandline only version:

.. code-block:: Bash

   python -m eldonationtracker.extralifedonations


Of course, you can import the modules into your own scripts and modify how you use the code I've written. In that case, you may be interested in the module index to get a good look at the API available to your program.
   
Commandline users (non-PyPi)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you downloaded a zip or tar file, unzip it first, then cd into that directory. If you did a git clone, cd in to that directory. Afterwards, follow along below to create a virtual environment (so as not to mess with your Python installation), grab the required packages, and run the program. (For information on what you should put into participant.conf, see :doc:`participant_conf`.

.. code-block:: Bash

    python3 -m venv .
    source ./bin/activate
    # when you are done using the program you can type deactivate
    pip install -r requirements.txt 
    # on Windows you may need to type python -m pip install -r requirements.txt
    # edit participant.conf 
    cd eldonationtracker
    # for the GUI:
    python gui.py
    # for the commandline only
    python extralifedonations.py

The benefit you get from using the GUI is that once the GUI comes up you can click "tracker" to get a window that will display an image and text when a donation is registered. For text instructions on how to use the GUI, go to :ref:`gui-usage` or watch the video at http://djotaku.github.io/ELDonationTracker/

eg:

.. image :: /images/tracker.gif

You can also edit the settings in a GUI rather than on the commandline. Once the settings are configured, hit the run button. You should get the same output on the commandline as you would if you weren't running the GUI. Check there for any errors or messages from the program.
