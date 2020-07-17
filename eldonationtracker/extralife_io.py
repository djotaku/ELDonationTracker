"""Holds all the file and internet input and output."""

import json
import os
import pathlib
import requests
from rich import print
import ssl
from typing import Tuple, Any
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

import xdgenvpy  # type: ignore


def validate_url(url: str):
    print(f"[bold blue]Checking: {url}[/bold blue]")
    response = requests.get(url)
    print(f"[bold magenta]Response is: {response.status_code}[/bold magenta]")
    if response.status_code == 200:
        return True
    else:
        return False


# JSON/URL
def get_json(url: str, order_by_donations: bool = False) -> dict:
    """Grab JSON from server.

    Connects to server and grabs JSON data from the specified URL. The API server should return JSON with the donation \
    data.

    :param url: API URL for the specific json API point.
    :param order_by_donations: If true, the url param has data appended that will cause the API to return the\
    data in descending order of the sum of donations.

    :return: JSON as dictionary with API data.

    :raises: HTTPError, URLError
    """
    payload = ""
    # context = ssl._create_default_https_context()
    context = ssl._create_unverified_context()
    header = {'User-Agent': 'Extra Life Donation Tracker'}
    if order_by_donations:
        url = url+"?orderBy=sumDonations%20DESC"
    try:
        request = Request(url=url, headers=header)
        payload = urlopen(request, timeout=5, context=context)
        #  print(f"trying URL: {url}")
        return json.load(payload)  # type: ignore
    except HTTPError:  # pragma no cover
        print(f"""[bold red]Could not get to {url}.
                Check ExtraLifeID.Or server may be unavailable.
                If you can reach that URL from your browser
                and this is not an intermittent problem, please open an issue at:
                https://github.com/djotaku/ELDonationTracker[/bold red]""")
        return {}
    except URLError:  # pragma no cover
        print(f"[bold red]HTTP code: {payload.getcode()}[/bold red]")  # type: ignore
        print(""" [bold red]Timed out while getting JSON. [/bold red]""")
        return {}

# File Input and Output
# input


class ParticipantConf:
    """Holds Participant Configuration info.

    :param cls.participant_conf_version: version of participant.conf
    :param cls.version_mismatch: Initialized to False.If true, the user has a different version of the participant.conf.
    :param cls.fields: A dictionary initialed to None for all fields.
    :param self.xdg: By using the PedanticPackage, the directory will be created if it doesn't already exist.
    :param self.participantconf: holds a dictionary of the user's config file.
    """

    participant_conf_version: str = "2.0"
    version_mismatch: bool = False
    fields: dict = {"extralife_id": None, "text_folder": None, "currency_symbol": None, "team_id": None,
                    "tracker_image": None, "donation_sound": None, "donors_to_display": None, "font_family": None,
                    "font_size": None, "font_italic": None, "font_bold": None, "font_color": None,
                    "tracker_background_color": None}

    def __init__(self):
        """Load in participant conf and check version."""
        self.xdg = xdgenvpy.XDGPedanticPackage('extralifedonationtracker')
        self.participantconf = self.load_json()
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
        self.xdg.XDG_CONFIG_HOME: str
        self.update_fields()

    def load_json(self) -> dict:  # pragma no cover
        """Load in the config file.

        Checks in a variety of locations for the participant.conf file.\
        First, it checks in the persistent settings location (XDG_CONFIG_HOME)\
        . Then it checks the current directory and one level up. Otherwise it\
        raises an exception and the program stops.

        :return: A dictionary representing the JSON config file.
        :raises: FileNotFoundError
        """

        try:
            print("[bold blue]Looking for persistent settings at "
                  f"{self.xdg.XDG_CONFIG_HOME}[/bold blue]")
            with open(f'{self.xdg.XDG_CONFIG_HOME}/participant.conf') as file:
                config = json.load(file)
                file.close()
                print("[bold green]Persistent settings found.[/bold green]")
            return config
        except FileNotFoundError:
            print("[bold magenta]Persistent settings not found. Checking current directory"
                  f"({os.getcwd()})[/bold magenta]")
        try:
            with open(pathlib.PurePath(__file__).parent.joinpath('.')/'participant.conf') as file:
                config = json.load(file)
                file.close()
            return config
        except FileNotFoundError:
            print("[bold magenta]Settings not found in current dir. Checking up one level.[/bold magenta]")
        try:
            with open(pathlib.PurePath(__file__).parent.joinpath('..')/'participant.conf') as file:
                config = json.load(file)
                file.close()
            return config
        except FileNotFoundError:
            self.get_github_config()
            return self.load_json()

    def get_github_config(self):  # pragma no cover
        print("[bold blue]Attempting to grab a config file from GitHub.[/bold blue]")
        print(f"[bold blue]Config will be placed at {self.xdg.XDG_CONFIG_HOME}.[/bold blue]")
        url = 'https://github.com/djotaku/ELDonationTracker/raw/master/participant.conf'
        try:
            config_file = requests.get(url)
            open(f"{self.xdg.XDG_CONFIG_HOME}/participant.conf", "wb").write(config_file.content)
        except HTTPError:
            print("[bold magenta] Could not find participant.conf on Github. [/bold magenta]"
                  "[bold magenta]Please manually create or download from Github.[/bold magenta]")

    def get_tracker_assets(self, asset: str):  # pragma no cover
        print(f"[bold blue] Attempting to grab {asset} from Github.[/bold blue] ")
        print(f"[bold blue] {asset} will be placed at the XDG location of: {self.xdg.XDG_DATA_HOME}[/bold blue] ")
        if asset == "image":
            url = 'https://raw.githubusercontent.com/djotaku/ELDonationTracker/master/tracker%20assets/Engineer.png'
        elif asset == "sound":
            url = 'https://raw.githubusercontent.com/djotaku/ELDonationTracker/master/tracker%20assets/Donation.mp3'
        try:
            file = requests.get(url)
            if asset == "image":
                open(f"{self.xdg.XDG_DATA_HOME}/{asset}.png", "wb").write(file.content)
                return f"{self.xdg.XDG_DATA_HOME}/{asset}.png"
            elif asset == "sound":
                open(f"{self.xdg.XDG_DATA_HOME}/{asset}.mp3", "wb").write(file.content)
                return f"{self.xdg.XDG_DATA_HOME}/{asset}.mp3"
            print("[bold blue]file written.[/bold blue]")
        except requests.HTTPError:
            print(f"[bold red]Could not get {asset}.[/bold red]")

    def update_fields(self):
        """Update fields variable with data from JSON."""
        for field in self.fields:
            self.fields[field] = self.participantconf.get(f'{field}')
            # debug
            # print(f"{field}:{self.fields[field]}")

    def write_config(self, config: dict, default: bool):  # pragma no cover
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
        self.reload_json()

    def get_version(self):
        """Return version."""
        return self.participant_conf_version

    def reload_json(self):
        """Reload JSON and update the fields."""
        self.participantconf = self.load_json()
        self.update_fields()

    def get_cli_values(self) -> Tuple[Any, Any, Any, Any, Any]:
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

    def get_gui_values(self) -> Tuple[Any, Any, Any, Any, Any, Any, Any, Any, Any, Any, Any, Any, Any]:
        """Return values needed for the GUI.

        :returns: A tuple of strings with config values needed if only\
        running the GUI. The two background colors are lists.
        """
        return (self.fields["extralife_id"], self.fields["text_folder"],
                self.fields["currency_symbol"], self.fields["team_id"],
                self.fields["tracker_image"], self.fields["donation_sound"],
                self.fields["donors_to_display"], self.fields["font_family"], self.fields["font_size"],
                self.fields["font_italic"], self.fields["font_bold"], self.fields["font_color"],
                self.fields["tracker_background_color"])

    def get_font_info(self):
        """Return values needed to change the font for the tracker.

        :returns: A tuple of strings and a list for the color.
        """
        return(self.fields["font_family"], self.fields["font_size"], self.fields["font_italic"],
               self.fields["font_bold"], self.fields["font_color"])

    def get_tracker_background_color(self):
        """Return value needed to change the tracker background color

        :returns: A list representing the RGB value for the background
        """
        return self.fields["tracker_background_color"]

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
        """Return bool of whether there is a version mismatch.

        :returns: True if the version the user is running is not the same as what this program has as its version.
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

    def __str__(self):
        return f"A configuration version {self.participant_conf_version} with the following data: {self.fields}"


# Formatting
def single_format(donor, message: bool, currency_symbol: str) -> str:
    """Format string for output to text file.

    This function is for when there is only one donor or donation.
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
        f.close()
