.. eldonationtracker documentation master file, created by
   sphinx-quickstart on Sun Feb 23 13:14:19 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to eldonationtracker's documentation!
=============================================

ELDonation Tracker is both a Python interface to the `Extra Life Charity`_ API and a reference implementation, including a GUI, that can be used to provide on-screen donation information and updates when streaming a gaming video or recording a gaming video in OBS or XSplit. For a video explaining how to use the GUI reference implementation, visit: http://djotaku.github.io/ELDonationTracker/ . You may also use the API to build your own applications that access the API. The modules are well documented, see the Module Index below.

.. note::

    Starting 20200227 this project will strictly follow Semantic Versioning as laid out at https://semver.org/ 
    
    That means:
    
    Given a version number MAJOR.MINOR.PATCH, increment the:
    
    #. MAJOR version when you make incompatible API changes,
    
    #. MINOR version when you add functionality in a backwards compatible manner, and
    
    #. PATCH version when you make backwards compatible bug fixes.


.. toctree::
   :maxdepth: 3
   :caption: Contents:

   installation
   usage
   participant_conf
   modules/call_about
   modules/call_settings
   modules/call_tracker
   modules/donation
   modules/donor
   modules/participant
   modules/extralife_io
   modules/gui
   modules/ipc
   modules/team
   modules/team_participant
   modules/utils/update_available
   


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _`Extra Life Charity`: https://www.extra-life.org