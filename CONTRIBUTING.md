Master will always contain perfectly working code aligned with the latest release.

If you wish to contribute, please do so off of the devel branch and file a pull request with your changes.

I am working on getting code up to PEP8 standards and writing unit tests. The following files should be without errors on flake8's test suite:

- extralifedonations.py

- IPC.py

- readparticipantconf.py

Because the PyQt classes and functions mimic their C/C++ classes and functions, they may violate PEP8 and other Python conventions, so flake8 does not have to pass on files related to the GUI. However, they should pass pydocstyle.

Once this is setup, the Github actions related to linting and unit tests must pass in order for a pull request to be accepted. (Subject, of course, to a waiver by me)
