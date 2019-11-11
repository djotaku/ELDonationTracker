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
        print(f""" Maybe have timed out. """)

# File Input and Output
# input


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
