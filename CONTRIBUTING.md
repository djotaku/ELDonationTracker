Master will always contain perfectly working code aligned with the latest release.

If you wish to contribute, please do so off of the devel branch and file a pull request with your changes. If I have another branch pushed to Github that may temporarily be the branch to develop from. Check with me.

The code is up to PEP8 standards and I have written unit tests. The following files should be without errors on flake8's test suite (don't worry about >80 char errors):

- donation.py

- donor.py

- extralifedonations.py

- extralife_IO.py

- IPC.py

- readparticipantconf.py

- team.py

All the unit tests in extralifeunittests.py should pass.

Because the PyQt classes and functions mimic their C/C++ classes and functions, they may violate PEP8 and other Python conventions, so flake8 does not have to pass on files related to the GUI. However, they should pass pydocstyle.

The Github actions related to linting and unit tests must pass in order for a pull request to be accepted. (Subject, of course, to a waiver by me)
