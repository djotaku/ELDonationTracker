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

.. todo:: 

    Add instructions and note that this could potentially cause problems with system packages.

User Install
------------

.. todo:: 

    Add Instructions

Via Github
^^^^^^^^^^

Here you have a few options depending on what you want to do.

GUI Single Executable Users
---------------------------

Go to the latest release_ and download the file that ends in "For Windows". Unzip it to the location you want to use and then proceed to :doc:`usage`.

Pyinstaller images will no longer be made for Linux as there are issues with the version of libC it links to as well as other side effects from the VM used by the Github CI system. Linux users can still use the GUI via PyPi, Source Code download, or git clone.

.. versionchanged:: 4.0.1


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
