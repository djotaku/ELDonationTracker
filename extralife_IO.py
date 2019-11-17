""" Holds all the file and internet input and output. """

import json
from urllib.request import Request, urlopen, HTTPError, URLError


# JSON/URL
def get_JSON(url, order_by_donations=False):
    """ Grab JSON from server.

    Connects to server and grabs JSON data from the specified URL.
    """
    header = {'User-Agent': 'Extra Life Donation Tracker'}
    if order_by_donations is True:
        url = url+"?orderBy=sumDonations%20DESC"
    # debug for 20191111 where having issues with API
    print(f"Trying to access URL: {url}")
    try:
        request = Request(url=url, headers=header)
        return json.load(urlopen(request))
    except HTTPError:
        print(f"""Couldn't get to {url}.
                Check ExtraLifeID.
                Or server may be unavailable.
                If you can reach that URL from your browser
                please open an issue at:
                https://github.com/djotaku/ELDonationTracker""")
    except URLError:
        print(f""" Timed out while getting JSON. """)

# File Input and Output
# input


class ParticipantConf:
    """ Holds Participant Configuaration info."""
    participant_conf_version = "1.0"
    version_mismatch = False
    fields = {"extralife_id": None, "text_folder": None,
              "currency_symbol": None, "team_id": None,
              "tracker_image": None,
              "donation_sound": None,
              "donors_to_display": None }

    def __init__(self):
        """ Load in participant conf and check version. """
        # fields = [self.extralife_id, self.text_folder, self.currency_symbol,
        #          self.team_id, self.tracker_image, self.donation_sound]
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
        with open('participant.conf') as file:
            config = json.load(file)
            file.close()
            return config

    def update_fields(self):
        for field in self.fields:
            self.fields[field] = self.participantconf.get(f'{field}')
            print(f"{field}:{self.fields[field]}")

    def get_version(self):
        return self.participant_conf_version

    def reload_JSON(self):
        self.participantconf = self.load_JSON()
        self.update_fields()

    def get_CLI_values(self):
        return (self.fields["extralife_id"], self.fields["text_folder"],
                self.fields["currency_symbol"],
                self.fields["team_id"])

    def get_text_folder_only(self):
        return self.fields["text_folder"]

    def get_GUI_values(self):
        return (self.fields["extralife_id"], self.fields["text_folder"],
                self.fields["currency_symbol"], self.fields["team_id"],
                self.fields["tracker_image"], self.fields["donation_sound"],
                self.fields["donors_to_display"])

    def get_version_mismatch(self):
        return self.version_mismatch

    def get_tracker_image(self):
        return self.fields["tracker_image"]

    def get_tracker_sound(self):
        return self.fields["donation_sound"]


# Formatting
def single_format(donor, message, currency_symbol):
    if message:
        return (f"{donor.name} - {currency_symbol}{donor.amount:.2f}"
                f" - {donor.message}")
    else:
        return f"{donor.name} - {currency_symbol}{donor.amount:.2f}"


def multiple_format(donors, message, horizontal, currency_symbol, how_many):
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
