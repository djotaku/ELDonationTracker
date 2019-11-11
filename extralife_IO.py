""" Holds all the file and internet input and output. """

import json
from urllib.request import Request, urlopen, HTTPError


# JSON/URL
def get_JSON(url):
    """ Grab JSON from server.

    Connects to server and grabs JSON data from the specified URL.
    """
    header = {'User-Agent': 'Extra Life Donation Tracker'}
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

# File Input and Output
# input


# Output
def write_text_files(dictionary, text_folder):
    """Write info to text files."""
    for filename, text in dictionary.items():
            f = open(f'{text_folder}/{filename}.txt', 'w', encoding='utf8')
            f.write(text)
            f.close
