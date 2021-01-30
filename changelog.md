#v6.0
## Release Notes

### User-Facing Changes

- To launch the command-line version of the program you now run: python -m eldonationtracker.cli

### Developer-Facing or API Changes

- Created Properties for accessing the variables for the API classes.
These also replace any "getter" methods that had been in place. 
  If there are no "setter" methods, it's because that attribute should
  only be set by internal methods and/or from the Donor Drive API. If you 
  believe an attribute without a "setter" should have one - 
  file an issue.
  
- re-organized files into sub-modules to better encapsulate which part of the program they are for.  All the Donor Drive API compoments are now found in eldonationtracker.api.  


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
