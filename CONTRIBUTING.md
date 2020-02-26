# Branches

Master should always contain perfectly working code aligned with the latest release.

If you wish to contribute, please do so off of the devel branch and file a pull request with your changes. If I have another branch pushed to Github, that branch may temporarily be the branch to develop from. Check with me.

# Linting (ie PEP8 Compliance)

I strive for the code to be PEP8 compliant. Run the following against your fork:

flake8 eldonationtracker/extralifedonations.py eldonationtracker/ipc.py eldonationtracker/readparticipantconf.py eldonationtracker/team.py eldonationtracker/donation.py eldonationtracker/donor.py eldonationtracker/extralife_IO.py  --count --select=E9,F63,F7,F82 --show-source --statistics

If it fails, the CI will fail and the pull request will not be merged until it is fixed. 

The next line will report warnings, but as long as it's only warnings and not errors, it will not stop the CI. That said, my preference is for the following to be error free (don't worry about line-length errors):

flake8 extralifedonations.py IPC.py readparticipantconf.py team.py donation.py donor.py extralife_IO.py --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics 

But even my code isn't (as of 26 Jan 2020) 100% perfect against that flake8 run, yet.

If that list above becomes out of date, the canonical list of files that need to pass flake8 can be found in the repo under .github/workflows/linttest.yml.

## About line-length

My preference is to try and stay *at least* within the Github max-line-length of 127. But I prefer readability to PEP8 perfection (which, I think is still at 80 chars, anyway)

## PyQt

Because the PyQt classes and functions mimic their C/C++ classes and functions, they may violate PEP8 and other Python conventions, so flake8 does not have to pass on files related to the GUI. However, they should pass pydocstyle.

# Testing

All the unit tests should pass. Run: pytest -v --pyargs eldonationtracker
