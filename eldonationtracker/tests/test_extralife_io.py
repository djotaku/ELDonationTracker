# This unit test test uses the following encoding: utf-8

from unittest import mock

from eldonationtracker import extralife_io
from eldonationtracker import donation


fields_for_participant_conf = {"extralife_id": "12345",
                               "text_folder": "textfolder",
                               "currency_symbol": "$",
                               "team_id": "45678",
                               "tracker_image": "imagefolder",
                               "donation_sound": "mp3",
                               "donors_to_display": "5",
                               "font_family": "Liberation Sans",
                               "font_size": 52, "font_italic": True, "font_bold": 25,
                               "font_color": [255, 255, 255, 255], "tracker_background_color": [38, 255, 0, 255]
                               }

fields_for_participant_conf_no_team = {"extralife_id": "12345",
                                       "text_folder": "textfolder",
                                       "currency_symbol": "$",
                                       "team_id": None,
                                       "tracker_image": "imagefolder",
                                       "donation_sound": "mp3",
                                       "donors_to_display": "5",
                                       "font_family": "Liberation Sans",
                                       "font_size": 52, "font_italic": True, "font_bold": 25,
                                       "font_color": [255, 255, 255, 255], "tracker_background_color": [38, 255, 0, 255]
                                       }


# validate_url tests
def test_validate_url_valid_url():
    """Test that a response code of 200 returns True."""
    class FakeResponse:
        def __init__(self):
            self.status_code = 200
    fake_requests_get_valid = mock.Mock()
    fake_requests_get_valid.return_value = FakeResponse()
    with mock.patch.object(extralife_io.requests, "get", fake_requests_get_valid):
        valid_url = extralife_io.validate_url("https://github.com/djotaku/ELDonationTracker")
        assert valid_url is True


def test_validate_url_invalid_url():
    """Test that a response code that isn't 200 returns False."""
    class FakeResponse:
        def __init__(self):
            self.status_code = 404
    fake_requests_get_valid = mock.Mock()
    fake_requests_get_valid.return_value = FakeResponse()
    with mock.patch.object(extralife_io.requests, "get", fake_requests_get_valid):
        invalid_url = extralife_io.validate_url("https://github.com/djotaku/ELDonationTracker")
        assert invalid_url is False


# get_json tests
mock_request = mock.Mock()
mock_url_open = mock.Mock()
mock_json_load = mock.Mock()


@mock.patch.object(extralife_io, 'Request', mock_request)
@mock.patch.object(extralife_io, 'urlopen', mock_url_open)
@mock.patch.object(extralife_io.json, 'load', mock_json_load)
def test_get_json_url_works_order_by_donations_false():
    extralife_io.get_json("https://github.com/djotaku/ELDonationTracker", False)
    mock_request.assert_called_with(url="https://github.com/djotaku/ELDonationTracker",
                                    headers={'User-Agent': 'Extra Life Donation Tracker'})


@mock.patch.object(extralife_io, 'Request', mock_request)
@mock.patch.object(extralife_io, 'urlopen', mock_url_open)
@mock.patch.object(extralife_io.json, 'load', mock_json_load)
def test_get_json_url_works_order_by_donations_true():
    extralife_io.get_json("https://github.com/djotaku/ELDonationTracker", True)
    mock_request.assert_called_with(url="https://github.com/djotaku/ELDonationTracker?orderBy=sumDonations%20DESC",
                                    headers={'User-Agent': 'Extra Life Donation Tracker'})


#@mock.patch.object(extralife_io, 'Request', mock_request)
#@mock.patch.object(extralife_io, 'urlopen', mock_url_open)
#@mock.patch.object(extralife_io.json, 'load', mock_json_load)
#def test_get_json_http_error_order_by_donations_false():
#    mock_request.side_effect = Exception(extralife_io.HTTPError)
#    extralife_io.get_json("https://github.com/djotaku/ELDonationTracker", False)
#    mock_request.assert_called_with(url="https://github.com/djotaku/ELDonationTracker",
#                                    headers={'User-Agent': 'Extra Life Donation Tracker'})


# ParticipantConf class - will need to figure out how to over-ride conf file
def test_version_mismatch():
    with mock.patch.object(extralife_io.ParticipantConf, "load_json", return_value={"Version": "1.0"}):
        participant_conf = extralife_io.ParticipantConf()
        assert participant_conf.version_mismatch is True


def test_participantconf_get_version():
    """Test that it correctly returns the version string."""
    participant_conf = extralife_io.ParticipantConf()
    assert "2.0" == participant_conf.get_version()


def test_reload_json():
    """Test that the fields are correct after a reload.

    First test that the fields start loaded above. Then that they are filled in.
    """
    with mock.patch.object(extralife_io.ParticipantConf,
                           "load_json",
                           return_value={'Version': '2.0', 'extralife_id': '12345', 'text_folder': 'textfolder'}):
        participant_conf = extralife_io.ParticipantConf()
        assert participant_conf.fields['extralife_id'] is "12345"
        assert participant_conf.fields['text_folder'] is "textfolder"
        # now let's change them.
        participant_conf.fields['extralife_id'] = "78900"
        participant_conf.fields['text_folder'] = "nottextfolder"
        # now reload and it should be back to where it was.
        participant_conf.reload_json()
        assert participant_conf.fields['extralife_id'] is "12345"
        assert participant_conf.fields['text_folder'] is "textfolder"


def test_participantconf_get_cli_values():
    """Test that the program correctly returns the CLI values."""
    participant_conf = extralife_io.ParticipantConf()
    participant_conf.fields = fields_for_participant_conf
    assert ("12345", "textfolder",
            "$", "45678", "5") == participant_conf.get_cli_values()


def test_get_text_folder_only():
    """Test that the text folder is correctly returned."""
    participant_conf = extralife_io.ParticipantConf()
    participant_conf.fields = fields_for_participant_conf
    assert "textfolder" == participant_conf.get_text_folder_only()


def test_get_gui_values():
    """Test that it correctly returns the values needed by the GUI."""
    participant_conf = extralife_io.ParticipantConf()
    participant_conf.fields = fields_for_participant_conf
    assert ("12345", "textfolder",
            "$", "45678", "imagefolder",
            "mp3", "5", "Liberation Sans", 52, True, 25, [255, 255, 255, 255],
            [38, 255, 0, 255]) == participant_conf.get_gui_values()


def test_get_font_info():
    """Test that it correctly returns the font information."""
    participant_conf = extralife_io.ParticipantConf()
    participant_conf.fields = fields_for_participant_conf
    assert ("Liberation Sans", 52, True, 25, [255, 255, 255, 255]) == participant_conf.get_font_info()


def test_get_tracker_background_color():
    """Test that it correctly returns the tracker's background color"""
    participant_conf = extralife_io.ParticipantConf()
    participant_conf.fields = fields_for_participant_conf
    assert [38, 255, 0, 255] == participant_conf.get_tracker_background_color()


def test_get_if_in_team_with_team():
    """Make sure that if there is a team in the config file,\
    it returns true."""
    participant_conf = extralife_io.ParticipantConf()
    participant_conf.fields = fields_for_participant_conf
    assert participant_conf.get_if_in_team() is True


def test_get_if_in_team_without_team():
    """Make sure that if there isn't a team, it repots there isn't\
    one defined."""
    participant_conf = extralife_io.ParticipantConf()
    participant_conf.fields = fields_for_participant_conf_no_team
    assert participant_conf.get_if_in_team() is False


def test_get_version_mismatch():
    participant_conf = extralife_io.ParticipantConf()
    assert participant_conf.get_version_mismatch() is False


def test_get_version_mismatch_if_mismatch():
    with mock.patch.object(extralife_io.ParticipantConf, "load_json", return_value={"Version": "1.0"}):
        participant_conf = extralife_io.ParticipantConf()
        assert participant_conf.get_version_mismatch() is True


def test_get_tracker_image():
    """Test that it returns the image location."""
    participant_conf = extralife_io.ParticipantConf()
    participant_conf.fields = fields_for_participant_conf
    assert "imagefolder" == participant_conf.get_tracker_image()


def test_get_tracker_sound():
    """Test that it returns the sound file location."""
    participant_conf = extralife_io.ParticipantConf()
    participant_conf.fields = fields_for_participant_conf
    assert "mp3" == participant_conf.get_tracker_sound()


def test_single_format_message_true():
    """ Make sure the formatting works correctly."""
    donor1 = donation.Donation("donor1", "message", 45, "4939d", "http://image.png", "2020-02-11T17:22:23.963+0000",
                               "861A3C59D235B4DA")
    currency_symbol = "$"
    formatted_message = extralife_io.single_format(donor1, True, currency_symbol)
    assert formatted_message == "donor1 - $45.00 - message"


def test_donor_formatting_message_false():
    """ Make sure the formatting works correctly without a message."""
    donor1 = donation.Donation("donor1", "message", 45, "4939d", "http://image.png", "2020-02-11T17:22:23.963+0000",
                               "861A3C59D235B4DA")
    currency_symbol = "$"
    formatted_message = extralife_io.single_format(donor1, False, currency_symbol)
    assert formatted_message == "donor1 - $45.00"


def test_participant_conf_str():
    participant_conf = extralife_io.ParticipantConf()
    participant_conf.fields = fields_for_participant_conf
    assert str(participant_conf) == """A configuration version 2.0 with the following data: {'extralife_id': '12345', 'text_folder': 'textfolder', 'currency_symbol': '$', 'team_id': '45678', 'tracker_image': 'imagefolder', 'donation_sound': 'mp3', 'donors_to_display': '5', 'font_family': 'Liberation Sans', 'font_size': 52, 'font_italic': True, 'font_bold': 25, 'font_color': [255, 255, 255, 255], 'tracker_background_color': [38, 255, 0, 255]}"""


donor1 = donation.Donation("donor1", "message1", 10, "4939d", "http://image.png", "2020-02-11T17:22:23.963+0000",
                           "861A3C59D235B4DA")
donor2 = donation.Donation("donor2", "message2", 20, "4939d", "http://image.png", "2020-02-11T17:22:23.963+0000",
                           "861A3C59D235B4DA")
donor3 = donation.Donation("donor3", "message3", 30, "4939d", "http://image.png", "2020-02-11T17:22:23.963+0000",
                           "861A3C59D235B4DA")
donor4 = donation.Donation("donor4", "message4", 40, "4939d", "http://image.png", "2020-02-11T17:22:23.963+0000",
                           "861A3C59D235B4DA")
donor5 = donation.Donation("donor5", "message5", 50, "4939d", "http://image.png", "2020-02-11T17:22:23.963+0000",
                           "861A3C59D235B4DA")
donor6 = donation.Donation("donor6", "message6", 60, "4939d", "http://image.png", "2020-02-11T17:22:23.963+0000",
                           "861A3C59D235B4DA")

def test_multiple_format_Horizontal():
    """Test formatting with multiple donations with increasing amounts\
    of donors to ensure the right string would be written to the file."""
    donor_list = [donor1, donor2, donor3, donor4, donor5, donor6]
    currency_symbol = "$"
    text1 = extralife_io.multiple_format(donor_list, False, True,
                                         currency_symbol, 1)
    text2 = extralife_io.multiple_format(donor_list, False, True,
                                         currency_symbol, 2)
    text3 = extralife_io.multiple_format(donor_list, False, True, currency_symbol, 3)
    text4 = extralife_io.multiple_format(donor_list, False, True,
                                         currency_symbol, 4)
    text5 = extralife_io.multiple_format(donor_list, False, True,
                                         currency_symbol, 5)
    textlist = [text1, text2, text3, text4, text5]
    assert textlist == ["donor1 - $10.00 | ",
                        "donor1 - $10.00 | donor2 - $20.00 | ",
                        "donor1 - $10.00 | donor2 - $20.00 | donor3 - $30.00 | ",
                        "donor1 - $10.00 | donor2 - $20.00 | donor3 - $30.00 | donor4 - $40.00 | ",
                        "donor1 - $10.00 | donor2 - $20.00 | donor3 - $30.00 | donor4 - $40.00 | donor5 - $50.00 | "]


def test_multiple_format_Message_Horizontal():
    """Test formatting with multiple donations with increasing amounts\
    of donors to ensure the right string would be written to the file.

    This time including the message that goes along with the donation.
    """
    donor_list = [donor1, donor2, donor3, donor4, donor5, donor6]
    currency_symbol = "$"
    text1 = extralife_io.multiple_format(donor_list, True, True,
                                         currency_symbol, 1)
    text2 = extralife_io.multiple_format(donor_list, True, True,
                                         currency_symbol, 2)
    text3 = extralife_io.multiple_format(donor_list, True, True, currency_symbol, 3)
    text4 = extralife_io.multiple_format(donor_list, True, True,
                                         currency_symbol, 4)
    text5 = extralife_io.multiple_format(donor_list, True, True,
                                         currency_symbol, 5)
    textlist = [text1, text2, text3, text4, text5]
    assert textlist == ["donor1 - $10.00 - message1 | ",
                        "donor1 - $10.00 - message1 | donor2 - $20.00 - message2 | ",
                        "donor1 - $10.00 - message1 | donor2 - $20.00 - message2 | donor3 - $30.00 - message3 | ",
                        "donor1 - $10.00 - message1 | donor2 - $20.00 - message2 | donor3 - $30.00 - message3 | donor4 - $40.00 - message4 | ",
                        "donor1 - $10.00 - message1 | donor2 - $20.00 - message2 | donor3 - $30.00 - message3 | donor4 - $40.00 - message4 | donor5 - $50.00 - message5 | "]


def test_multiple_format_Vertical():
    """Test formatting with multiple donations with increasing amounts\
    of donors to ensure the right string would be written to the file."""
    donor_list = [donor1, donor2, donor3, donor4, donor5, donor6]
    currency_symbol = "$"
    text1 = extralife_io.multiple_format(donor_list, False, False,
                                         currency_symbol, 1)
    text2 = extralife_io.multiple_format(donor_list, False, False,
                                         currency_symbol, 2)
    text3 = extralife_io.multiple_format(donor_list, False, False, currency_symbol, 3)
    text4 = extralife_io.multiple_format(donor_list, False, False,
                                         currency_symbol, 4)
    text5 = extralife_io.multiple_format(donor_list, False, False,
                                         currency_symbol, 5)
    textlist = [text1, text2, text3, text4, text5]
    assert textlist == ["donor1 - $10.00\n",
                        "donor1 - $10.00\ndonor2 - $20.00\n",
                        "donor1 - $10.00\ndonor2 - $20.00\ndonor3 - $30.00\n", 
                        "donor1 - $10.00\ndonor2 - $20.00\ndonor3 - $30.00\ndonor4 - $40.00\n",
                        "donor1 - $10.00\ndonor2 - $20.00\ndonor3 - $30.00\ndonor4 - $40.00\ndonor5 - $50.00\n"]


def test_multiple_format_Message_Vertical():
    """Test formatting with multiple donations with increasing amounts\
    of donors to ensure the right string would be written to the file.

    This time including the message that goes along with the donation.
    """
    donor_list = [donor1, donor2, donor3, donor4, donor5, donor6]
    currency_symbol = "$"
    text1 = extralife_io.multiple_format(donor_list, True, False,
                                         currency_symbol, 1)
    text2 = extralife_io.multiple_format(donor_list, True, False,
                                         currency_symbol, 2)
    text3 = extralife_io.multiple_format(donor_list, True, False, currency_symbol, 3)
    text4 = extralife_io.multiple_format(donor_list, True, False,
                                         currency_symbol, 4)
    text5 = extralife_io.multiple_format(donor_list, True, False,
                                         currency_symbol, 5)
    textlist = [text1, text2, text3, text4, text5]
    assert textlist == ["donor1 - $10.00 - message1\n",
                        "donor1 - $10.00 - message1\ndonor2 - $20.00 - message2\n",
                        "donor1 - $10.00 - message1\ndonor2 - $20.00 - message2\ndonor3 - $30.00 - message3\n",
                        "donor1 - $10.00 - message1\ndonor2 - $20.00 - message2\ndonor3 - $30.00 - message3\ndonor4 - $40.00 - message4\n",
                        "donor1 - $10.00 - message1\ndonor2 - $20.00 - message2\ndonor3 - $30.00 - message3\ndonor4 - $40.00 - message4\ndonor5 - $50.00 - message5\n"]


def test_write_text_files():
    """ Test that data gets written to the text files correctly. """
    fileinput = ""
    dictionary = {"testfilename": "test output"}
    text_folder = "testOutput"
    extralife_io.write_text_files(dictionary, text_folder)
    with open(f"testOutput/testfilename.txt") as file:
        fileinput = file.read()
    assert fileinput == "test output"


def test_write_text_files_unicode():
    """ Test that unicode gets written to the text files correctly. """
    fileinput = ""
    dictionary = {"testfilename": "áéíóúñ"}
    text_folder = "testOutput"
    extralife_io.write_text_files(dictionary, text_folder)
    with open(f"testOutput/testfilename.txt", 'r', encoding='utf8') as file:
        fileinput = file.read()
    assert fileinput == "áéíóúñ"


def test_write_text_files_emoji():
    """ Test that emojis get written to the text files correctly. """
    fileinput = ""
    dictionary = {"testfilename": "😁😂🧐🙏🚣🌸🦞🏰💌"}
    text_folder = "testOutput"
    extralife_io.write_text_files(dictionary, text_folder)
    with open(f"testOutput/testfilename.txt", 'r', encoding='utf8') as file:
        fileinput = file.read()
    assert fileinput == "😁😂🧐🙏🚣🌸🦞🏰💌"
