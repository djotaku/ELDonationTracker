"""Holds all the file and internet input and output."""

import json
import pathlib
import ssl
from urllib.request import HTTPError, Request, URLError, urlopen

import xdgenvpy


# JSON/URL
def get_JSON(url, order_by_donations=False):
    """Grab JSON from server.

    Connects to server and grabs JSON data from the specified URL.
    """
    payload = ""
    # context = ssl._create_default_https_context()
    context = ssl._create_unverified_context()
    header = {'User-Agent': 'Extra Life Donation Tracker'}
    if order_by_donations is True:
        url = url+"?orderBy=sumDonations%20DESC"
    # debug when having issues with API
    # print(f"Trying to access URL: {url}")
    try:
        request = Request(url=url, headers=header)
        payload = urlopen(request, timeout=5, context=context)
        # debug if having connection issues
        # print(f"HTTP code: {payload.getcode()}")
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
    """Holds Participant Configuaration info."""

    participant_conf_version = "1.0"
    version_mismatch = False
    fields = {"extralife_id": None, "text_folder": None,
              "currency_symbol": None, "team_id": None,
              "tracker_image": None,
              "donation_sound": None,
              "donors_to_display": None}

    def __init__(self):
        """Load in participant conf and check version."""
        # fields = [self.extralife_id, self.text_folder, self.currency_symbol,
        #          self.team_id, self.tracker_image, self.donation_sound]
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

    def load_JSON(self):
        """Load in the config file."""
        # by using pedantic, it'll create the directory if it's not there

        try:
            print(f"Looking for persistent settings at {self.xdg.XDG_CONFIG_HOME}")
            with open(f'{self.xdg.XDG_CONFIG_HOME}/participant.conf') as file:
                config = json.load(file)
                file.close()
                print("Persistent settings found.")
            return config
        except FileNotFoundError:
            print("Persistent settings not found. Checking current directory")
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
            print("Giving up. Put settings in current directory.")

    def update_fields(self):
        """Update fields with data from JSON."""
        for field in self.fields:
            self.fields[field] = self.participantconf.get(f'{field}')
            # debug
            # print(f"{field}:{self.fields[field]}")

    def write_config(self, config, default):
        """Write config to file.

        At this point, only called from GUI. Commandline
        user is expected to edit file manually.
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

    def get_CLI_values(self):
        """Return data required for a CLI-only run."""
        return (self.fields["extralife_id"], self.fields["text_folder"],
                self.fields["currency_symbol"],
                self.fields["team_id"], self.fields["donors_to_display"])

    def get_text_folder_only(self):
        """Return text folder data."""
        return self.fields["text_folder"]

    def get_GUI_values(self):
        """Return values needed for the GUI."""
        return (self.fields["extralife_id"], self.fields["text_folder"],
                self.fields["currency_symbol"], self.fields["team_id"],
                self.fields["tracker_image"], self.fields["donation_sound"],
                self.fields["donors_to_display"])

    def get_if_in_team(self):
        """Return True if participant is in a team."""
        # debug
        # print(self.fields["team_id"])
        if self.fields["team_id"] is None:
            return False
        else:
            return True

    def get_version_mismatch(self):
        """Return bool of whether there is a version mismatch."""
        return self.version_mismatch

    def get_tracker_image(self):
        """Return the tracker image location on disk."""
        return self.fields["tracker_image"]

    def get_tracker_sound(self):
        """Return the donation sound image location on disk."""
        return self.fields["donation_sound"]


# Formatting
def single_format(donor, message, currency_symbol):
    """Take donor, bool of whether it has a message, and a currency symbol. Then return formatted text for creating the output files."""
    if message:
        return (f"{donor.name} - {currency_symbol}{donor.amount:.2f}"
                f" - {donor.message}")
    else:
        return f"{donor.name} - {currency_symbol}{donor.amount:.2f}"


def multiple_format(donors, message, horizontal, currency_symbol, how_many):
    """Create text for multi-donor output files."""
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
def write_text_files(dictionary, text_folder):
    """Write info to text files."""
    for filename, text in dictionary.items():
        f = open(f'{text_folder}/{filename}.txt', 'w', encoding='utf8')
        f.write(text)
        f.close
