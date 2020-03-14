"""Holds all the file and internet input and output."""

import json
import os
import pathlib
import requests
import ssl
from typing import Tuple
from urllib.request import HTTPError, Request, URLError, urlopen

import xdgenvpy


# JSON/URL
def get_JSON(url: str, order_by_donations: bool = False) -> dict:
    """Grab JSON from server.

    Connects to server and grabs JSON data from the specified URL.\
    The API server should return JSON with the donation data.

    :param url: API URL for the specific json API point.
    :param order_by_donations: If true, the url param has\
    has text appended that will cause the API to return the\
    data in descending order of the sum of donations.

    :return: JSON as dictionary with API data.

    :raises: HTTPError, URLError
    """
    payload = ""
    # context = ssl._create_default_https_context()
    context = ssl._create_unverified_context()
    header = {'User-Agent': 'Extra Life Donation Tracker'}
    if order_by_donations is True:
        url = url+"?orderBy=sumDonations%20DESC"
    try:
        request = Request(url=url, headers=header)
        payload = urlopen(request, timeout=5, context=context)
        #  print(f"trying URL: {url}")
        return json.load(payload)
    except HTTPError:
        print(f"""Couldn't get to {url}.
                Check ExtraLifeID.
                Or server may be unavailable.
                If you can reach that URL from your browser
                and this is not an intermittent issue:
                please open an issue at:
                https://github.com/djotaku/ELDonationTracker""")
        return 0  # to be proper this should return an exemption
    except URLError:
        print(f"HTTP code: {payload.getcode()}")
        print(f""" Timed out while getting JSON. """)
        return 0

# File Input and Output
# input


class ParticipantConf:
    """Holds Participant Configuaration info.

    :param participant_conf_version: version of participant.conf
    :param version_mismatch: Initialized to False.If true, the\
    user has a different version of the participant.conf.
    :param fields: A dictionary initialed to None for all fields.
    :param xdg: By using the PedanticPackage, the directory will\
    be created if it doesn't already exist.
    :param participantconf: holds a dictionary of the user's\
    config file.
    """

    participant_conf_version: str = "1.0"
    version_mismatch: bool = False
    fields: dict = {"extralife_id": None, "text_folder": None,
                    "currency_symbol": None, "team_id": None,
                    "tracker_image": None,
                    "donation_sound": None,
                    "donors_to_display": None}

    def __init__(self):
        """Load in participant conf and check version."""
        self.xdg = xdgenvpy.XDGPedanticPackage('extralifedonationtracker')
        self.participantconf = self.load_JSON()
        if self.participantconf['Version'] != self.participant_conf_version:
            print(f"You are using an old version of participant.conf.\n"
                  f"Your version is: {self.participantconf['Version']}\n"
                  f"Current Version is {self.participant_conf_version}.\n"
                  f"If you are on the commandline, check to see what"
                  f" has changed and add it to your configuration file."
                  f" You will likely have an error later because of this.\n"
                  f"If you are in the GUI, it should prompt you to"
                  f" Migrate or start fresh.")
            self.version_mismatch = True
        self.update_fields()

    def load_JSON(self) -> dict:
        """Load in the config file.

        Checks in a variety of locations for the participant.conf file.\
        First, it checks in the persistent settings location (XDG_CONFIG_HOME)\
        . Then it checks the current directory and one level up. Otherwise it\
        raises an exception and the program stops.

        :return: A dictionary representing the JSON config file.
        :raises: FileNotFoundError
        """

        try:
            print("Looking for persistent settings at "
                  f"{self.xdg.XDG_CONFIG_HOME}")
            with open(f'{self.xdg.XDG_CONFIG_HOME}/participant.conf') as file:
                config = json.load(file)
                file.close()
                print("Persistent settings found.")
            return config
        except FileNotFoundError:
            print("Persistent settings not found. Checking current directory"
                  f"({os.getcwd()})")
        try:
            with open(pathlib.PurePath(__file__).parent.joinpath('.')/'participant.conf') as file:
                config = json.load(file)
                file.close()
            return config
        except FileNotFoundError:
            print("Settings not found in current dir. Checking up one level.")
        try:
            with open(pathlib.PurePath(__file__).parent.joinpath('..')/'participant.conf') as file:
                config = json.load(file)
                file.close()
            return config
        except FileNotFoundError:
            print("Attempting to grab a config file from github.")
            print(f"Config will be placed at {self.xdg.XDG_CONFIG_HOME}.")
            url = 'https://github.com/djotaku/ELDonationTracker/raw/master/participant.conf'
            config_file = requests.get(url)
            open(f"{self.xdg.XDG_CONFIG_HOME}/participant.conf", "wb").write(config_file.content)
            return self.load_JSON()
            #with open(f'{self.xdg.XDG_CONFIG_HOME}/participant.conf') as file:
                #config = json.load(file)
                #file.close()
            #return config

    def update_fields(self):
        """Update fields variable with data from JSON."""
        for field in self.fields:
            self.fields[field] = self.participantconf.get(f'{field}')
            # debug
            # print(f"{field}:{self.fields[field]}")

    def write_config(self, config: dict, default: bool):
        """Write config to file.

        Only called from GUI. Commandline user is expected to edit\
        participant.conf manually. Afterward it triggers self.reloadJSON\
        to have the program run with the updated config.

        :param config: A dictionary holding the config values.
        :param default: If True, will save the file in the current directory.
        """
        if default:
            with open('participant.conf', 'w') as outfile:
                json.dump(config, outfile)
        else:
            with open(f'{self.xdg.XDG_CONFIG_HOME}/participant.conf', 'w') as outfile:
                json.dump(config, outfile)
        self.reload_JSON()

    def get_version(self):
        """Return version."""
        return self.participant_conf_version

    def reload_JSON(self):
        """Reload JSON and update the fields."""
        self.participantconf = self.load_JSON()
        self.update_fields()

    def get_CLI_values(self) -> Tuple[str, int]:
        """Return data required for a CLI-only run.

        :returns: A tuple of strings with config values needed if only\
        running on the commandline.
        """
        return (self.fields["extralife_id"], self.fields["text_folder"],
                self.fields["currency_symbol"],
                self.fields["team_id"], self.fields["donors_to_display"])

    def get_text_folder_only(self) -> str:
        """Return text folder data.

        :returns: A string with the text folder location."""
        return self.fields["text_folder"]

    def get_GUI_values(self) -> Tuple[str, int]:
        """Return values needed for the GUI.

        :returns: A tuple of strings with config values needed if only\
        running the GUI
        """
        return (self.fields["extralife_id"], self.fields["text_folder"],
                self.fields["currency_symbol"], self.fields["team_id"],
                self.fields["tracker_image"], self.fields["donation_sound"],
                self.fields["donors_to_display"])

    def get_if_in_team(self) -> bool:
        """Return True if participant is in a team.

        :returns: True if the participant is in a team.
        """
        # debug
        # print(self.fields["team_id"])
        if self.fields["team_id"] is None:
            return False
        else:
            return True

    def get_version_mismatch(self) -> bool:
        """Return bool of whether there is a version mismatch.0

        :returns: True if the version the user is running is not\
        the same as what this program has as its version.
        """
        return self.version_mismatch

    def get_tracker_image(self) -> str:
        """Return the tracker image location on disk.

        :returns: Location of tracker image on disk.
        """
        return self.fields["tracker_image"]

    def get_tracker_sound(self) -> str:
        """Return the donation sound image location on disk.

        :returns: location of the donation sound on disk.
        """
        return self.fields["donation_sound"]


# Formatting
def single_format(donor, message: bool, currency_symbol: str) -> str:
    """Format string for output to text file.

    This function is for when there is only one donor or donation.\
    For example, for the text file holding the most recent donation.

    :param donor: Donor or Donation class object.
    :param message: If True, the message (if any) from the donor object\
    :param currency_symbol: The currency symbol to append to the return string.
    :returns: A string containing the inputs formatted. For example: \n
    John Doe - $100.00 - Thanks for raising money for the kids.
    """
    if message:
        return (f"{donor.name} - {currency_symbol}{donor.amount:.2f}"
                f" - {donor.message}")
    else:
        return f"{donor.name} - {currency_symbol}{donor.amount:.2f}"


def multiple_format(donors, message: bool, horizontal: bool,
                    currency_symbol: str, how_many: int) -> str:
    """Format string for output to text file.

    This function is for when there is are multiple donors or donations.\
    For example, for the text file holding the Top 5 donors.

    :param donors: An iterable of Donors or Donations class objects.
    :param message: If True, the message (if any) from the donor object\
    :param horizontal: If True, format the message horizontally. Else\
    vertically.
    :param currency_symbol: The currency symbol to append to the return string.
    :param how_many: A number for how many donors/donations to append to the\
    string.
    :returns: A string containing the inputs formatted.\n
    Horizontal example: \n
    John Doe - $100.00 - Thanks for raising money for the kids. |\
    Jane Doe - $25.00 - Hurray!\n\n
    Vertical example: \n
    John Doe - $200.00 - a message\n
    Jane Doe - $75.00 - another message
    """
    text = ""
    if horizontal:
        for donor in range(0, len(donors)):
            text = text+single_format(donors[donor],
                                      message,
                                      currency_symbol)+" | "
            if donor == how_many - 1:
                break
        return text
    else:
        for donor in range(0, len(donors)):
            text = text+single_format(donors[donor],
                                      message,
                                      currency_symbol)+"\n"
            if donor == how_many - 1:
                break
        return text


# Output
def write_text_files(dictionary: dict, text_folder: str):
    """Write info to text files.

    The dictionary key will become the filename and the values will\
    be the content of the files.

    :param dictionary: The dictionary with items to output.
    :param text_folder: The directory to write the text files.
    """
    for filename, text in dictionary.items():
        f = open(f'{text_folder}/{filename}.txt', 'w', encoding='utf8')
        f.write(text)
        f.close
