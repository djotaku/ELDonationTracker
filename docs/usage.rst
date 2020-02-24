=====
Usage
=====

GUI users
^^^^^^^^^

Documentation to be added

Commandline users (PyPi)
^^^^^^^^^^^^^^^^^^^^^^^^

Will be filled out once PyPi is working

Commandline users (non-PyPi)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you downloaded a zip or tar file, unzip it first, then cd into that directory. Afterwards, follow along below to create a virtual environment (so as not to mess with your Python installation), grab the required packages, and run the program. 

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

The benefit you get from using the GUI is that once the GUI comes up you can click "tracker" to get a window that will display an image and text when a donation is registered. You can also edit the settings in a GUI rather than on the commandline. To run the program, hit the run button. You should get the same output on the commandline as you would if you weren't running the GUI. Check there for any errors.
