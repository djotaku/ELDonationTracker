=====
Usage
=====

GUI Single Executable users
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This refers to you if you downloaded a file like Extra Life Donation Tracker for Windows v3.4.zip. 

.. todo:: 

    Add documentation on how to use it, include images.

Commandline users (PyPi)
^^^^^^^^^^^^^^^^^^^^^^^^

Go to the folder you created in :doc:`installation`. If you don't have the virtual environment activated, start with that:

.. code-block:: Bash

    python3 -m venv .
    source ./bin/activate
    # to check for upgrades
    pip install --upgrade eldonationtracker


**GUI**

Make sure you have the :doc:`participant_conf` in the persistent location. You can grab the one in the Github repo or create your own by looking at the example there. Once the GUI has actually started, you can easily modify the config file via the GUI. To start the GUI:

.. code-block:: Bash

   python -m eldonationtracker.gui
   
That should work just fine. Keep an eye on the commandline for any errors or messages from eldonationtracker. The benefit you get from using the GUI is that once the GUI comes up you can click "tracker" to get a window that will display an image and text when a donation is registered. 

eg:

.. image :: /images/tracker.gif

You can also edit the settings in a GUI rather than on the commandline.   

**Commandline Only (No GUI)**

Make sure you have the :doc:`participant_conf` in the persistent location. You can grab the one in the Github repo or create your own by looking at the example there. To start the commandline only version:

.. code-block:: Bash

   python -m python -m eldonationtracker.extralifedonations


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

The benefit you get from using the GUI is that once the GUI comes up you can click "tracker" to get a window that will display an image and text when a donation is registered. 

eg:

.. image :: /images/tracker.gif

You can also edit the settings in a GUI rather than on the commandline. Once the settings are configured, hit the run button. You should get the same output on the commandline as you would if you weren't running the GUI. Check there for any errors or messages from the program.
