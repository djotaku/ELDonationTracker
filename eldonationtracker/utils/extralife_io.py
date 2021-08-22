"""Holds all the file and internet input and output."""

import json
import logging
import os
import pathlib
import requests
from rich import print
from rich.logging import RichHandler
from typing import Tuple, Any

import xdgenvpy  # type: ignore

from eldonationtracker import api_version_suffix
from eldonationtracker.api.donation import Donation
from eldonationtracker.api.donor import Donor
from eldonationtracker.api.badge import Badge  # type: ignore

# logging
el_io_log = logging.getLogger("ExtraLife IO")
el_io_log.setLevel(logging.INFO)


def validate_url(url: str):
    el_io_log.debug(f"[bold blue]Checking: {url}[/bold blue]")
    response = requests.get(url)
    el_io_log.debug(f"[bold magenta]Response is: {response.status_code}[/bold magenta]")
    return response.status_code == 200


# JSON/URL
def get_json(url: str, order_by_donations: bool = False, order_by_amount: bool = False) -> dict:
    """Grab JSON from server.

    Connects to server and grabs JSON data from the specified URL. The API server should return JSON with the donation \
    data.

    :param url: API URL for the specific json API point.
    :param order_by_donations: If true, the url param has data appended that will cause the API to return the\
    data in descending order of the sum of donations.
    :param order_by_amount: If true, the url param has data appended that will cause the API to return the\
    data in descending order of the sum of amounts.

    :return: JSON as dictionary with API data.

    :raises: ConnectionError, Timeout
    """
    header = {'User-Agent': 'Extra Life Donation Tracker'}
    response = None
    if order_by_donations and not order_by_amount:
        url += "?orderBy=sumDonations%20DESC"
    elif order_by_amount:
        url += "?orderBy=amount%20DESC"
    else:
        url += api_version_suffix
    try:
        el_io_log.debug(url)
        response = requests.get(url=url, headers=header)
        return response.json()  # type: ignore
    except requests.exceptions.ConnectionError as this_error:  # pragma: no cover
        el_io_log.error(f"""[bold red]Could not get to {url}.
                Exact error was: {this_error}.
                Check ExtraLifeID. Or server may be unavailable.
                If you can reach that URL from your browser
                and this is not an intermittent problem, please open an issue at:
                https://github.com/djotaku/ELDonationTracker[/bold red]""")
        return {}
    except requests.exceptions.Timeout:  # pragma: no cover
        el_io_log.error(f"[bold red]HTTP code: {response.status_code}[/bold red]")  # type: ignore
        el_io_log.error("[bold red]Timed out while getting JSON. [/bold red]")
        return {}


def get_donations(donations_or_donors: list, api_url: str, is_donation=True, largest_first=False) -> list:
    """Get the donations from the JSON and create the donation objects.

    If the API can't be reached, the same list is returned. Only new donations are added to the list at the end.

    :param is_donation: True if we are getting data for donations. False if we are getting data for donors.
    :param largest_first: True if we want to sort by largest. False if sort by latest donors or donations.
    :param donations_or_donors: A list consisting of donation.Donation or donor.Donor objects.
    :param api_url: The URL to go to for donations.
    :returns: A list of donation.Donation objects.
    """
    if largest_first and is_donation:
        json_response = get_json(api_url, largest_first, is_donation)
    else:
        json_response = get_json(api_url, largest_first)
    if not json_response:
        el_io_log.error(f"[bold red]Couldn't access JSON endpoint at {api_url}.[/bold red]")
        return donations_or_donors
    else:
        if is_donation:
            donor_or_donation_list = [Donation(this_donation) for this_donation in json_response]
        else:
            donor_or_donation_list = [Donor(this_donor) for this_donor in json_response]  # type: ignore
        if len(donations_or_donors) == 0:  # if I didn't already have donations....
            return donor_or_donation_list
        else:  # add in only the new donations
            for a_donation in reversed(donor_or_donation_list):
                if a_donation not in donations_or_donors:
                    donations_or_donors.insert(0, a_donation)
            return donations_or_donors


def get_badges(api_url: str) -> list[Badge]:
    """Get badges from the API endpoint and create a list to return.

    :param api_url: The URL for the API endpoint.
    :returns: A list of badges.
    """
    json_response = get_json(api_url)
    return [Badge.create_badge(badge_item) for badge_item in json_response]


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
            el_io_log.warning(f"You are using an old version of participant.conf.\n"
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

    def load_json(self) -> dict:  # pragma: no cover
        """Load in the config file.

        Checks in a variety of locations for the participant.conf file.\
        First, it checks in the persistent settings location (XDG_CONFIG_HOME)\
        . Then it checks the current directory and one level up. Otherwise it\
        raises an exception and the program stops.

        :return: A dictionary representing the JSON config file.
        :raises: FileNotFoundError
        """

        try:
            el_io_log.info(f"[bold blue]Looking for persistent settings at {self.xdg.XDG_CONFIG_HOME}[/bold blue]")
            with open(f'{self.xdg.XDG_CONFIG_HOME}/participant.conf') as file:
                config = json.load(file)
                file.close()
                el_io_log.info("[bold green]Persistent settings found.[/bold green]")
            return config
        except FileNotFoundError:
            el_io_log.warning("[bold magenta]Persistent settings not found. Checking current directory"
                              f"({os.getcwd()})[/bold magenta]")
        try:
            with open(pathlib.PurePath(__file__).parent.joinpath('.') / 'participant.conf') as file:
                config = json.load(file)
                file.close()
            return config
        except FileNotFoundError:
            el_io_log.warning("[bold magenta]Settings not found in current dir. Checking up one level.[/bold magenta]")
        try:
            with open(pathlib.PurePath(__file__).parent.joinpath('..') / 'participant.conf') as file:
                config = json.load(file)
                file.close()
            return config
        except FileNotFoundError:
            self.get_github_config()
            return self.load_json()

    def get_github_config(self):  # pragma: no cover
        el_io_log.info("[bold blue]Attempting to grab a config file from GitHub.[/bold blue]")
        el_io_log.info(f"[bold blue]Config will be placed at {self.xdg.XDG_CONFIG_HOME}.[/bold blue]")
        url = 'https://github.com/djotaku/ELDonationTracker/raw/master/participant.conf'
        try:
            config_file = requests.get(url)
            open(f"{self.xdg.XDG_CONFIG_HOME}/participant.conf", "wb").write(config_file.content)
        except requests.exceptions.HTTPError:
            el_io_log.error("[bold magenta] Could not find participant.conf on Github. [/bold magenta]"
                            "[bold magenta]Please manually create or download from Github.[/bold magenta]")

    def get_tracker_assets(self, asset: str):  # pragma: no cover
        el_io_log.info(f"[bold blue] Attempting to grab {asset} from Github.[/bold blue] ")
        el_io_log.info(f"[bold blue] {asset} will be placed at the XDG location of: {self.xdg.XDG_DATA_HOME}[/bold "
                       f"blue] ")
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
            el_io_log.info("[bold blue]file written.[/bold blue]")
        except requests.exceptions.HTTPError:
            el_io_log.error(f"[bold red]Could not get {asset}.[/bold red]")

    def update_fields(self):
        """Update fields variable with data from JSON."""
        for field in self.fields:
            self.fields[field] = self.participantconf.get(f'{field}')
            el_io_log.debug(f"{field}:{self.fields[field]}")

    def write_config(self, config: dict, default: bool):  # pragma: no cover
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
        return (self.fields["font_family"], self.fields["font_size"], self.fields["font_italic"],
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
        el_io_log.debug(self.fields["team_id"])
        return self.fields["team_id"] is not None

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
    for donor in range(len(donors)):
        if horizontal:
            text = text + single_format(donors[donor],
                                        message,
                                        currency_symbol) + " | "
        else:
            text = text + single_format(donors[donor],
                                        message,
                                        currency_symbol) + "\n"
        if donor == how_many - 1:
            break
    return text


def format_information_for_output(donation_list: list, currency_symbol: str, donors_to_display: str, team: bool,
                                  donation=True) -> dict:
    """Format the donation attributes for the output files.

    :param donation:
    :param donation_list: A list of donors or donations to format for output.
    :type donation_list: list
    :param currency_symbol: The currency symbol for the output.
    :param donors_to_display: How many donors or donations to display
    :param team: If true, this is creating output for a team. Otherwise, for the participant.
    :returns: A dictionary with the output text formatted correctly.
    """
    donation_formatted_output: dict = {}
    prefix = "Team_" if team else ''
    middle_text = "Donation" if donation else "Donor"
    donation_formatted_output[f'{prefix}Last{middle_text}NameAmnt'] = single_format(donation_list[0],
                                                                                    False, currency_symbol)
    donation_formatted_output[f'{prefix}lastN{middle_text}NameAmts'] = \
        multiple_format(donation_list, False, False, currency_symbol, int(donors_to_display))
    if donation:
        donation_formatted_output[f'{prefix}lastN{middle_text}NameAmtsMessage'] = \
            multiple_format(donation_list, True, False, currency_symbol, int(donors_to_display))
        donation_formatted_output[f'{prefix}lastN{middle_text}NameAmtsMessageHorizontal'] = \
            multiple_format(donation_list, True, True, currency_symbol, int(donors_to_display))
    donation_formatted_output[f'{prefix}lastN{middle_text}NameAmtsHorizontal'] = \
        multiple_format(donation_list, False, True, currency_symbol, int(donors_to_display))
    return donation_formatted_output


def output_badge_data(badge_list: list[Badge], text_folder: str, team=False) -> None:  # pragma: no cover
    """Write out text and HTML files for badge data."""
    prefix = ''
    if team:
        prefix = "team_"
    if badge_list:
        badge_text_output = {}
        badge_url_output = {}
        for a_badge in badge_list:
            badge_text_output[f"{prefix}{a_badge.badge_code}"] = f"{a_badge.title}: {a_badge.description}"
            badge_url_output[f"{prefix}{a_badge.badge_code}"] = f"<img src='{a_badge.badge_image_url}'>"
        badge_text_folder = f"{text_folder}badges/text/"
        write_text_files(badge_text_output, badge_text_folder)
        badge_image_folder = f"{text_folder}badges/images/"
        for badge_image_filename, badge_image_url in badge_url_output.items():
            write_html_files(badge_image_url, badge_image_filename, badge_image_folder)


def read_in_total_raised(text_folder: str) -> str:
    """This is a temporary hack until I resolve Github issue #162"""
    try:
        with open(f'{text_folder}/totalRaised.txt', 'r', encoding='utf8') as total_raised:
            return total_raised.readline()
    except FileNotFoundError:
        el_io_log.info("[bold blue] totalRaised.txt doesn't exist. This is OK if this is your first run. [/bold blue]")
        return ""


# Output
def write_text_files(dictionary: dict, text_folder: str):
    """Write info to text files.

    The dictionary key will become the filename and the values will\
    be the content of the files.

    :param dictionary: The dictionary with items to output.
    :param text_folder: The directory to write the text files.
    """
    try:
        os.makedirs(text_folder)
    except FileExistsError:
        pass
    for filename, text in dictionary.items():
        with open(f'{text_folder}/{filename}.txt', 'w', encoding='utf8') as file:
            file.write(text)


def write_html_files(data: str, filename: str, text_folder: str):
    """Write data to an HTML file.

    :param data: The data to write to an HTML file.
    :param filename: The filename for the HTML file.
    :param text_folder: The directory to write the HTML files to.
    """
    try:
        os.mkdir(text_folder)
    except FileExistsError:
        pass
    html_to_write = "<HTML><body>" + data + "</body></HTML>"
    with open(f'{text_folder}/{filename}.html', 'w', encoding='utf8') as html_file:
        html_file.write(html_to_write)
