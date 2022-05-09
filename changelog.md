# v7.2.0
## Release Notes
### User-Facing Changes
- Added a GUI with log output.

### Developer-Facing or API Changes
- Nothing, really


# v7.1.0
## Release Notes
### User-Facing Changes
- Text file creation should work better now on a new year where there haven't been any donations yet.

### Developer-Facing or API Changes
- Updated to [DonorDrivePython 1.3.0](https://github.com/djotaku/DonorDrivePython) which should provide even better error reporting.


# v7.0.2
## Release Notes
### User-Facing Changes
- Nothing has changed for the user

### Developer-Facing or API Changes
- Updated to [DonorDrivePython 1.2.0](https://github.com/djotaku/DonorDrivePython) which should provide better error reporting.

# v7.0.1
## Release Notes
### User-Facing Changes
- Nothing has changed for the user

### Developer-Facing or API Changes
- Updated to [DonorDrivePython 1.1.1](https://github.com/djotaku/DonorDrivePython) which should prevent a crash if the JSON comes had a decoder error.

# v7.0.0
## Release Notes
### User-Facing Changes
- Nothing has changed for the user

### Developer-Facing or API Changes
- moved most of the API code to [DonorDrivePython](https://github.com/djotaku/DonorDrivePython) to abstract it away from Extra Life so it can be used by others using the DonorDrive API.

# v6.2.2
## Release Notes
### User-Facing Changes
- API pegging code had messed up Top Donor code that is now fixed
- Fix bug upon loading if user has > $999.99 in donations

### Developer-Facing or API Changes
- cleaned up logging code in utils.extralifeio


# v6.2.1
## Release Notes
### User-Facing Changes
- A fix so that the font changes for the tracker window that are saved in preferences are applied upon startup..

### Developer-Facing or API Changes
- cleaned up some duplicate code in call_tracker.py
- cleaned up logging code

# v6.2
## Release Notes
### User-Facing Changes

### Developer-Facing or API Changes
- Move from urllib to requests
- Pegged DonorDrive API version

# v6.1.2
## Release Notes
### User-Facing Changes
- Should not overwrite your text files if the API can't be reached
- changed many of the print statements to log output using Rich's logging

### Developer-Facing or API Changes

# v6.1.1
## Release Notes
### User-Facing Changes
- None

### Developer-Facing or API Changes
- Because Donor API is empty if user only has Anonymous donors, changed handling of Donors slightly

# v6.1.0
## Release Notes
### User-Facing Changes
- Badge Output files: See the subfolder badges within your output folder. There is an images folder with HTML so you can display the images.
- Milestone Output files: In your output folder look for text files that start with milestone
- Incentive Output files: In your output folder there will be a subfolder called invencitves. Within there is a folder per incentive you have. There you will find text files and, if you have images, HTML files.


### Developer-Facing or API Changes
- Badge API endpoint for both teams and participants now available
- Milestone API now available for participants
- Incentive API now available for participants

# v6.0.2
## Release Notes
### User-Facing Changes
None

### Developer-Facing or API Changes
- The string "http:" is no longer prepended to Particpant and Team Avatar URLs.

# v6.0
## Release Notes

### User-Facing Changes

- To launch the command-line version of the program you now run: python -m eldonationtracker.cli

- New output files: LastDonorNameAmnt.txt, lastNDonorNameAmtsHorizontal.txt,lastNDonorNameAmts.txt, TopDonationNameAmnt.txt

### Developer-Facing or API Changes

- Created Properties for accessing the variables for the API classes.
These also replace any "getter" methods that had been in place.
  If there are no "setter" methods, it's because that attribute should
  only be set by internal methods and/or from the Donor Drive API. If you
  believe an attribute without a "setter" should have one -
  file an issue.

- re-organized files into sub-modules to better encapsulate which part of the program they are for.  All the Donor Drive API compoments are now found in eldonationtracker.api.

- Now getting all the attributes for the Participant, Team, Donor, and Donation. We aren't currently pushing all of these out to text files for the user, but can be used if you want to use this package as a Python API for your own programs.


# v5.3.0
## Release Notes

### User-Facing Changes

- There are two new output files: Participant_Avatar.html and Team_Avatar.html. Feel free to use them in OBS, XSplit, or anywhere else to make your overlay more personalized.
- added Participant Avatar to the GUI
- Added Docker (or you can use Podman) Container

### Developer-Facing or API Changes

- Updated the version of PyQt and associated libraries.


# v5.2.4
## Release Notes

### User-Facing Changes

- Fix issue #137 where Emojis in the donor name cause a crash

### Developer-Facing or API Changes

None. If you are coming from a pre-5.0 version, please see: https://github.com/djotaku/ELDonationTracker/releases/tag/v5.2.0
