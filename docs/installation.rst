============
Installation
============


Via PyPi
^^^^^^^^

Eventually I will have the proper GH CI setup to automatically create PyPi packages. Until then, see below.

Via Github
^^^^^^^^^^

Here you have a few options depending on what you want to do.

**GUI Single Executable Users**

Go to the latest release_ and download the file that ends in "For Windows" or "For Linux" (depending on your platform, obviously). Unzip or untar it to the location you want to use and then proceed to :doc:`usage`.

.. _release: https://github.com/djotaku/ELDonationTracker/releases

**Commandline Users and/or Developers**

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
