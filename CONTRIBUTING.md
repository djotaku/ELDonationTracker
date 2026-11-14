# Branches

Master should always contain perfectly working code aligned with the latest release.

If you wish to contribute, please do and file a pull request with your changes. If I have another branch pushed to Github, that branch may temporarily be the branch to develop from. Check with me.

# Linting (ie PEP8 Compliance)

I strive for the code to be PEP8 compliant. Run the following against your fork:

```bash
uvx ruff check src/eldonationtracker/api src/eldonationtracker/utils
```

## About line-length

My preference is to try and stay *at least* within the Github max-line-length of 127. But I prefer readability to PEP8 perfection (which, I think is still at 80 chars, anyway)

# Testing

All the unit tests should pass. Run: pytest -v --pyargs eldonationtracker

Coverage:  coverage run -m pytest --pyargs eldonationtracker

# Documentation

It's important to keep documentation up to date. So make sure docstrings reflect any changes made to the code. It's processed by Sphinx, so adhere to its superset of restructured text format. You can find the latest documentation at: https://eldonationtracker.readthedocs.io/en/latest/ and the module auto-documentation might be easier to read there than going through the code.
