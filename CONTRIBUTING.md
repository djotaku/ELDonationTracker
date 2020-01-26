Master will always contain perfectly working code aligned with the latest release.

If you wish to contribute, please do so off of the devel branch and file a pull request with your changes. If I have another branch pushed to Github that may temporarily be the branch to develop from. Check with me.

I strive for the code to be PEP8 compliant. Run the following against your fork:

flake8 extralifedonations.py IPC.py readparticipantconf.py team.py donation.py donor.py extralife_IO.py --count --select=E9,F63,F7,F82 --show-source --statistics

If it fails, the CI will fail and the pull request will not be merged until it is fixed. 

My preference is for the following to be error free (don't worry about line-length errors):

flake8 extralifedonations.py IPC.py readparticipantconf.py team.py donation.py donor.py extralife_IO.py --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics 

But even my code isn't (as of 26 Jan 2020) perfect against that flake8 run, yet.

If that list above becomes out of date, the canonical list of files that need to pass flake8 can be found in the repo under .github/workflows/linttest.yml.

All the unit tests in extralifeunittests.py should pass.

Because the PyQt classes and functions mimic their C/C++ classes and functions, they may violate PEP8 and other Python conventions, so flake8 does not have to pass on files related to the GUI. However, they should pass pydocstyle.

The Github actions related to linting and unit tests must pass in order for a pull request to be accepted. (Subject, of course, to a waiver by me)
