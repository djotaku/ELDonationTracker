#v6.w.2
## Release Notes
### User-Facing Changes

### Developer-Facing or API Changes
- Move from urllib to requests
- Pegged DonorDrive API version

#v6.1.2
## Release Notes
### User-Facing Changes
- Should not overwrite your text files if the API can't be reached
- changed many of the print statements to log output using Rich's logging 

### Developer-Facing or API Changes

#v6.1.1
## Release Notes
### User-Facing Changes
- None

### Developer-Facing or API Changes
- Because Donor API is empty if user only has Anonymous donors, changed handling of Donors slightly

#v6.1.0
## Release Notes
### User-Facing Changes
- Badge Output files: See the subfolder badges within your output folder. There is an images folder with HTML so you can display the images.
- Milestone Output files: In your output folder look for text files that start with milestone
- Incentive Output files: In your output folder there will be a subfolder called invencitves. Within there is a folder per incentive you have. There you will find text files and, if you have images, HTML files.


### Developer-Facing or API Changes
- Badge API endpoint for both teams and participants now available
- Milestone API now available for participants
- Incentive API now available for participants

#v6.0.2
## Release Notes
### User-Facing Changes
None

### Developer-Facing or API Changes
- The string "http:" is no longer prepended to Particpant and Team Avatar URLs.

#v6.0
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


#v5.3.0
## Release Notes

### User-Facing Changes

- There are two new output files: Participant_Avatar.html and Team_Avatar.html. Feel free to use them in OBS, XSplit, or anywhere else to make your overlay more personalized.
- added Participant Avatar to the GUI
- Added Docker (or you can use Podman) Container

### Developer-Facing or API Changes

- Updated the version of PyQt and associated libraries.


#v5.2.4
## Release Notes

### User-Facing Changes

- Fix issue #137 where Emojis in the donor name cause a crash

### Developer-Facing or API Changes

None. If you are coming from a pre-5.0 version, please see: https://github.com/djotaku/ELDonationTracker/releases/tag/v5.2.0
