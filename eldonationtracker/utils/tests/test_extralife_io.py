# This unit test test uses the following encoding: utf-8
# type: ignore

import json
from unittest import mock

from eldonationtracker.utils import extralife_io
from eldonationtracker.api import donation
from eldonationtracker.api import donor

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
mock_requests = mock.Mock()


@mock.patch.object(extralife_io.requests, 'get', mock_requests)
def test_get_json_url_works_order_by_donations_false():
    extralife_io.get_json("https://github.com/djotaku/ELDonationTracker", False)
    mock_requests.assert_called_with(url="https://github.com/djotaku/ELDonationTracker?version=1.2",
                                     headers={'User-Agent': 'Extra Life Donation Tracker'})


@mock.patch.object(extralife_io.requests, 'get', mock_requests)
def test_get_json_url_works_order_by_donations_true():
    extralife_io.get_json("https://github.com/djotaku/ELDonationTracker", True)
    mock_requests.assert_called_with(url="https://github.com/djotaku/ELDonationTracker?orderBy=sumDonations%20DESC",
                                     headers={'User-Agent': 'Extra Life Donation Tracker'})


@mock.patch.object(extralife_io.requests, 'get', mock_requests)
def test_get_json_url_works_order_by_amount_true():
    extralife_io.get_json("https://github.com/djotaku/ELDonationTracker", False, True)
    mock_requests.assert_called_with(url="https://github.com/djotaku/ELDonationTracker?orderBy=amount%20DESC",
                                     headers={'User-Agent': 'Extra Life Donation Tracker'})


badge_example_json = """[
{
    "description": "Raised 100 dollars!",
    "title": "100 Club Badge",
    "unlockedDateUTC": "2019-10-30T18:01:23.430+0000",
    "badgeImageURL": "http://assets.donordrive.com/try/images/$event508$/badge_2F7819D3_C019_3C7D_B9D716687CEEC0A5.png",
    "badgeCode": "100-club-badge"
  },
  {
    "description": "Sent 25 donation invite emails!",
    "title": "Enthusiastic Participant Badge",
    "unlockedDateUTC": "2019-09-18T15:47:39.107+0000",
    "badgeImageURL": "https://assets.donordrive.com/try/images/$event508$/badge_DCB0A883_BC0A_97DB_639B4D7BFDEC638E.png",
    "badgeCode": "enthusiastic-participant-badge"
  }
]"""


@mock.patch.object(extralife_io, "get_json", return_value=json.loads(badge_example_json))
def test_get_badges(something):
    """Test that badges are retrieved and returned as a list."""
    test_badges = extralife_io.get_badges("fake_url")
    print(test_badges)
    assert test_badges[0].badge_code == "100-club-badge"
    assert test_badges[1].badge_code == "enthusiastic-participant-badge"


@mock.patch.object(extralife_io, 'get_json', return_value=json.loads('[]'))
def test_get_badges_no_badges(something):
    """Test that badges are retrieved and returned as a list."""
    test_badges = extralife_io.get_badges("fake_url")
    assert test_badges == []


fake_donations = {"displayName": "Sean Gibson", "participantID": 401280, "amount": 25.00, "donorID": "54483486D840B7EA",
                  "avatarImageURL": "//assets.donordrive.com/clients/extralife/img/avatar-constituent-default.gif",
                  "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                  "donationID": "861A3C59D235B4DA"}, {"displayName": "Eric Mesa", "participantID": 401280,
                                                      "amount": 25.00, "donorID": "4162ECD2B8BF4C17",
                                                      "avatarImageURL": "//assets.overdrive.com/extralife/images/$avat"
                                                                        "ars$/constituent_D4DC394A-C293-34EB-4162ECD2B"
                                                                        "8BF4C17.jpg",
                                                      "createdDateUTC": "2020-01-05T20:35:28.897+0000",
                                                      "eventID": 547, "teamID": 50394, "donationID": "7D430E9E9AF79686"}
donation1_json = {"displayName": "Donor 1", "participantID": '4939d', "amount": 34.51, "donorID": "FAKE3C59D235B4DA",
                  "avatarImageURL": "//image.png", "message": "Good job!",
                  "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                  "donationID": "861A3C59D235B4DB"}
donation1 = donation.Donation(donation1_json)
fake_donor = {"sumDonations": "45", "donorID": 1000111, "avatarImageURL": "//someplace.com/image.jpg",
              "numDonations": 2}
donor1 = donor.Donor(fake_donor)
fake_extralife_io = mock.Mock()
fake_extralife_io.get_JSON_donations.return_value = fake_donations
fake_extralife_io.get_JSON_donors.return_value = fake_donor
fake_extralife_io.get_JSON_no_json.return_value = {}
fake_extralife_io.get_JSON_donations_no_json.return_value = {}
fake_extralife_io.get_JSON_top_donor_no_json.return_value = {}


@mock.patch.object(extralife_io, "get_json", fake_extralife_io.get_JSON_donations)
def test_get_donations():
    """Ensure that JSON is properly parsed to create the donation objects."""
    donation_list = []
    donations = extralife_io.get_donations(donation_list, "http://fakeurl.com")
    assert donations[0].name == "Sean Gibson"
    assert donations[0].donor_id == "54483486D840B7EA"
    assert donations[0].avatar_url == "//assets.donordrive.com/clients/extralife/img/avatar-constituent-default.gif"
    assert donations[0].donation_date == "2020-02-11T17:22:23.963+0000"
    assert donations[1].name == "Eric Mesa"


@mock.patch.object(extralife_io, "get_json", fake_extralife_io.get_JSON_donations_no_json)
def test_get_donations_no_json():
    """Test to make sure nothing goes wrong if the JSON endpoint can't be reached."""
    donation_list = []
    donations = extralife_io.get_donations(donation_list, "http://fakeurl.com")
    assert donations == []


@mock.patch.object(extralife_io, "get_json", fake_extralife_io.get_JSON_donations)
def test_get_donations_already_a_donation_present():
    donation_list = [donation1]
    donation_list = extralife_io.get_donations(donation_list, "http://fakeurl.com")
    assert donation_list[0].name == "Sean Gibson"
    assert donation_list[1].name == "Eric Mesa"
    assert donation_list[2].name == "Donor 1"


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
        assert participant_conf.fields['extralife_id'] == "12345"
        assert participant_conf.fields['text_folder'] == "textfolder"
        # now let's change them.
        participant_conf.fields['extralife_id'] = "78900"
        participant_conf.fields['text_folder'] = "nottextfolder"
        # now reload and it should be back to where it was.
        participant_conf.reload_json()
        assert participant_conf.fields['extralife_id'] == "12345"
        assert participant_conf.fields['text_folder'] == "textfolder"


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
    donor1 = donation.Donation(donation1_json)
    currency_symbol = "$"
    formatted_message = extralife_io.single_format(donor1, True, currency_symbol)
    assert formatted_message == "donor1 - $10.00 - message1"


def test_donor_formatting_message_false():
    """ Make sure the formatting works correctly without a message."""
    donor1 = donation.Donation(donation1_json)
    currency_symbol = "$"
    formatted_message = extralife_io.single_format(donor1, False, currency_symbol)
    assert formatted_message == "donor1 - $10.00"


def test_participant_conf_str():
    participant_conf = extralife_io.ParticipantConf()
    participant_conf.fields = fields_for_participant_conf
    assert str(participant_conf) == """A configuration version 2.0 with the following data: {'extralife_id': '12345', 'text_folder': 'textfolder', 'currency_symbol': '$', 'team_id': '45678', 'tracker_image': 'imagefolder', 'donation_sound': 'mp3', 'donors_to_display': '5', 'font_family': 'Liberation Sans', 'font_size': 52, 'font_italic': True, 'font_bold': 25, 'font_color': [255, 255, 255, 255], 'tracker_background_color': [38, 255, 0, 255]}"""


donation1_json = {"displayName": "donor1", "participantID": '4939d', "amount": 10, "message": "message1",
                               "donorID": "FAKE3C59D235B4DA", "avatarImageURL": "//image.png",
                               "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                               "donationID": "861A3C59D235B4DA"}
donation2_json = {"displayName": "donor2", "participantID": '4939d', "amount": 20, "message": "message2",
                               "donorID": "FAKE3C59D235B4DA", "avatarImageURL": "//image.png",
                               "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                               "donationID": "861A3C59D235B4DA"}
donation3_json = {"displayName": "donor3", "participantID": '4939d', "amount": 30, "message": "message3",
                               "donorID": "FAKE3C59D235B4DA", "avatarImageURL": "//image.png",
                               "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                               "donationID": "861A3C59D235B4DA"}
donation4_json = {"displayName": "donor4", "participantID": '4939d', "amount": 40, "message": "message4",
                               "donorID": "FAKE3C59D235B4DA", "avatarImageURL": "//image.png",
                               "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                               "donationID": "861A3C59D235B4DA"}
donation5_json = {"displayName": "donor5", "participantID": '4939d', "amount": 50, "message": "message5",
                               "donorID": "FAKE3C59D235B4DA", "avatarImageURL": "//image.png",
                               "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                               "donationID": "861A3C59D235B4DA"}
donation6_json = {"displayName": "donor6", "participantID": '4939d', "amount": 60, "message": "message6",
                               "donorID": "FAKE3C59D235B4DA", "avatarImageURL": "//image.png",
                               "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                               "donationID": "861A3C59D235B4DA"}

donor1 = donation.Donation(donation1_json)
donor2 = donation.Donation(donation2_json)
donor3 = donation.Donation(donation3_json)
donor4 = donation.Donation(donation4_json)
donor5 = donation.Donation(donation5_json)
donor6 = donation.Donation(donation6_json)


def test_multiple_format_horizontal():
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


def test_multiple_format_message_horizontal():
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
    text_list = [text1, text2, text3, text4, text5]
    assert text_list == ["donor1 - $10.00 - message1 | ",
                        "donor1 - $10.00 - message1 | donor2 - $20.00 - message2 | ",
                        "donor1 - $10.00 - message1 | donor2 - $20.00 - message2 | donor3 - $30.00 - message3 | ",
                        "donor1 - $10.00 - message1 | donor2 - $20.00 - message2 | donor3 - $30.00 - message3 | donor4 - $40.00 - message4 | ",
                        "donor1 - $10.00 - message1 | donor2 - $20.00 - message2 | donor3 - $30.00 - message3 | donor4 - $40.00 - message4 | donor5 - $50.00 - message5 | "]


def test_multiple_format_vertical():
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


def test_multiple_format_message_vertical():
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


def test_write_text_files(tmpdir):
    """ Test that data gets written to the text files correctly. """
    dictionary = {"test_filename": "test output"}
    extralife_io.write_text_files(dictionary, tmpdir)
    with open(f"{tmpdir}/test_filename.txt") as file:
        file_input = file.read()
    assert file_input == "test output"


def test_write_text_files_unicode(tmpdir):
    """ Test that unicode gets written to the text files correctly. """
    dictionary = {"test_filename": "áéíóúñ"}
    extralife_io.write_text_files(dictionary, tmpdir)
    with open(f"{tmpdir}/test_filename.txt", 'r', encoding='utf8') as file:
        file_input = file.read()
    assert file_input == "áéíóúñ"


def test_write_text_files_emoji(tmpdir):
    """ Test that emojis get written to the text files correctly. """
    dictionary = {"test_filename": "😁😂🧐🙏🚣🌸🦞🏰💌"}
    extralife_io.write_text_files(dictionary, tmpdir)
    with open(f"{tmpdir}/test_filename.txt", 'r', encoding='utf8') as file:
        file_input = file.read()
    assert file_input == "😁😂🧐🙏🚣🌸🦞🏰💌"


def test_write_html_files(tmpdir):
    """Test that the HTML files are writen correctly."""
    data = "data for HTML file"
    filename = "test_HTML"
    extralife_io.write_html_files(data, filename, tmpdir)
    with open(f"{tmpdir}/{filename}.html", 'r', encoding='utf8') as file:
        html_input = file.read()
    assert html_input == f"<HTML><body>{data}</body></HTML>"
