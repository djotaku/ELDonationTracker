# Branches

Master should always contain perfectly working code aligned with the latest release.

If you wish to contribute, please do and file a pull request with your changes. If I have another branch pushed to Github, that branch may temporarily be the branch to develop from. Check with me.

# Linting (ie PEP8 Compliance)

I strive for the code to be PEP8 compliant. Run the following against your fork:

flake8 eldonationtracker/api eldonationtracker/utils  --count --select=E9,F63,F7,F82 --show-source --statistics

If it fails, the CI will fail, and the pull request will not be merged until it is fixed.

The next line will report warnings, but as long as it's only warnings and not errors, it will not stop the CI. That said, my preference is for the following to be error free (don't worry about line-length errors):

flake8 eldonationtracker/api eldonationtracker/utils --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

## About line-length

My preference is to try and stay *at least* within the Github max-line-length of 127. But I prefer readability to PEP8 perfection (which, I think is still at 80 chars, anyway)

## PyQt

Because the PyQt classes and functions mimic their C/C++ classes and functions, they may violate PEP8 and other Python conventions, so flake8 does not have to pass on files related to the GUI. However, they should pass pydocstyle.

# Static Analysis

mypy eldonationtracker

Should pass without errors.

# Testing

All the unit tests should pass. Run: pytest -v --pyargs eldonationtracker

Coverage:  coverage run -m pytest --pyargs eldonationtracker

# Documentation

It's important to keep documentation up to date. So make sure docstrings reflect any changes made to the code. It's processed by Sphinx, so adhere to its superset of restructured text format. You can find the latest documentation at: https://eldonationtracker.readthedocs.io/en/latest/ and the module auto-documentation might be easier to read there than going through the code.
