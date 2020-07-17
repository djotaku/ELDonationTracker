============
Installation
============


Via PyPi
^^^^^^^^

The first thing to decide is whether you want to install ELDonationTracker to your system packages, user packages, or a virtual environment. 

Virtual Environment (recommended)
---------------------------------

Create the folder you want to work in and cd into it. 

.. code-block:: Bash

    python3 -m venv .
    source ./bin/activate
    # when you are done using the program you can type deactivate
    # first, make sure you have the latest pip, I've had trouble installing with old versions
    pip install --upgrade pip
    pip install eldonationtracker
    # on Windows you may need to type python -m pip install eldonationtracker
    # Grab participant.conf from git repo or create based on documentation
    # Place participant.conf in persistent location, see the page in documentation
    

System Packages
---------------

.. note::

    This is NOT recommended and can cause issues with your system.

.. code-block:: Bash

    sudo pip install --upgrade pip
    sudo pip install eldonationtracker
    # Grab participant.conf from git repo or create based on documentation
    # Place participant.conf in persistent location, see the page in documentation

User Install
------------

.. note::

    A user install is sometimes a bit buggier than either using a virtual environment or system packages

.. code-block:: Bash

    sudo pip install --upgrade pip
    sudo pip install eldonationtracker
    # Grab participant.conf from git repo or create based on documentation
    # Place participant.conf in persistent location, see the page in documentation

Via Github
^^^^^^^^^^

Here you have a few options depending on what you want to do.

GUI Windows Executable Users
----------------------------

Go to the latest release_ and download one of the files that ends in "For Windows". You can choose a single executable binary or a zip file. The single executable is simply launched like any Windows application - double-click it. It has a slower startup time than the zip file, but once it's running, there is no performance penalty. For the zip file: unzip it to the location you want to use and then proceed to :doc:`usage`.

.. versionadded:: 4.4.0
    Single-binary executable build added.

.. versionchanged:: 4.0.1
    Pyinstaller images will no longer be made for Linux as there are issues with the version of libC it links to as well as other side effects from the VM used by the Github CI system. Linux users can still use the GUI via PyPi, Source Code download, or git clone.


.. _release: https://github.com/djotaku/ELDonationTracker/releases

Commandline Users and/or Developers
-----------------------------------

Two options:

#. Go to the latest release_ and click on "Source Code (zip)" or "Source Code (tar.gz)" depending on whether you're using on Windows or Linux. Then proceed to :doc:`usage`.

#. Go to the main Github page_ and click on "Clone or Download" and click the button to copy the URL to your clipboard. Then run:

.. code-block:: Bash
    
    git clone https://github.com/djotaku/ELDonationTracker.git

    
And any time you want to get up to the latest version you can just go to that folder and type:

.. code-block:: Bash
    
    git pull
    
The master branch is always equivalent to the latest release (except maybe with more up-to-date documentation) so you should always end up with a working version of ELDonationTracker if you do a git pull. (As long as you're not changing any files. For that reason you may want to move your participant.conf to the persistent location - see :doc:`participant_conf` for that location) Then proceed to :doc:`usage`.

.. _page: https://github.com/djotaku/ELDonationTracker
