# This unitest test uses the following encoding: utf-8

from eldonationtracker import extralife_IO
from eldonationtracker import donation


fields_for_participant_conf = {"extralife_id": "12345",
                               "text_folder": "textfolder",
                               "currency_symbol": "$",
                               "team_id": "45678",
                               "tracker_image": "imagefolder",
                               "donation_sound": "mp3",
                               "donors_to_display": "5"}

fields_for_participant_conf_no_team = {"extralife_id": "12345",
                                       "text_folder": "textfolder",
                                       "currency_symbol": "$",
                                       "team_id": None,
                                       "tracker_image": "imagefolder",
                                       "donation_sound": "mp3",
                                       "donors_to_display": "5"}


# Tests for extralife_IO.py

# come back and do one for get_JSON

# ParticipantConf class - will need to figure out how to over-ride conf file
def test_participantconf_get_version():
    """Test that the version it reads from the participant.conf file\
    equals what is expected."""
    participant_conf = extralife_IO.ParticipantConf()
    assert "1.0" == participant_conf.get_version()


def test_participantconf_get_CLI_values():
    """Test that the program correctly returns the CLI values."""
    participant_conf = extralife_IO.ParticipantConf()
    participant_conf.fields = fields_for_participant_conf
    assert ("12345", "textfolder",
            "$", "45678", "5") == participant_conf.get_CLI_values()


def test_get_text_folder_only():
    """Test that the text folder is correctly returned."""
    participant_conf = extralife_IO.ParticipantConf()
    participant_conf.fields = fields_for_participant_conf
    assert "textfolder" == participant_conf.get_text_folder_only()


def test_get_GUI_values():
    """Test that it correctly returns the values needed by the GUI."""
    participant_conf = extralife_IO.ParticipantConf()
    participant_conf.fields = fields_for_participant_conf
    assert ("12345", "textfolder",
            "$", "45678", "imagefolder",
            "mp3", "5") == participant_conf.get_GUI_values()


def test_get_if_in_team_with_team():
    """Make sure that if there is a team in the config file,\
    it returns true."""
    participant_conf = extralife_IO.ParticipantConf()
    participant_conf.fields = fields_for_participant_conf
    assert participant_conf.get_if_in_team() is True


def test_get_if_in_team_without_team():
    """Make sure that if there isn't a team, it repots there isn't\
    one defined."""
    participant_conf = extralife_IO.ParticipantConf()
    participant_conf.fields = fields_for_participant_conf_no_team
    assert participant_conf.get_if_in_team() is False


def test_get_tracker_image():
    """Test that it returns the image location."""
    participant_conf = extralife_IO.ParticipantConf()
    participant_conf.fields = fields_for_participant_conf
    assert "imagefolder" == participant_conf.get_tracker_image()


def test_get_tracker_sound():
    """Test that it returns the sound file location."""
    participant_conf = extralife_IO.ParticipantConf()
    participant_conf.fields = fields_for_participant_conf
    assert "mp3" == participant_conf.get_tracker_sound()


def test_single_format_message_true():
    """ Make sure the formatting works correctly."""
    donor1 = donation.Donation("donor1", "message", 45)
    currency_symbol = "$"
    formatted_message = extralife_IO.single_format(donor1, True, currency_symbol)
    assert formatted_message == "donor1 - $45.00 - message"


def test_donor_formatting_message_false():
    """ Make sure the formatting works correctly without a message."""
    donor1 = donation.Donation("donor1", "message", 45)
    currency_symbol = "$"
    formatted_message = extralife_IO.single_format(donor1, False, currency_symbol)
    assert formatted_message == "donor1 - $45.00"


def test_multiple_format_Horizontal():
    """Test formatting with multiple donations with increasing amounts\
    of donors to ensure the right string would be written to the file."""
    donor1 = donation.Donation("donor1", "message1", 10)
    donor2 = donation.Donation("donor2", "message2", 20)
    donor3 = donation.Donation("donor3", "message3", 30)
    donor4 = donation.Donation("donor4", "message4", 40)
    donor5 = donation.Donation("donor5", "message5", 50)
    donor6 = donation.Donation("donor6", "message6", 60)
    donor_list = [donor1, donor2, donor3, donor4, donor5, donor6]
    currency_symbol = "$"
    text1 = extralife_IO.multiple_format(donor_list, False, True,
                                         currency_symbol, 1)
    text2 = extralife_IO.multiple_format(donor_list, False, True,
                                         currency_symbol, 2)
    text3 = extralife_IO.multiple_format(donor_list,                                   False, True, currency_symbol, 3)
    text4 = extralife_IO.multiple_format(donor_list, False, True,
                                         currency_symbol, 4)
    text5 = extralife_IO.multiple_format(donor_list, False, True,
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
    donor1 = donation.Donation("donor1", "message1", 10)
    donor2 = donation.Donation("donor2", "message2", 20)
    donor3 = donation.Donation("donor3", "message3", 30)
    donor4 = donation.Donation("donor4", "message4", 40)
    donor5 = donation.Donation("donor5", "message5", 50)
    donor6 = donation.Donation("donor6", "message6", 60)
    donor_list = [donor1, donor2, donor3, donor4, donor5, donor6]
    currency_symbol = "$"
    text1 = extralife_IO.multiple_format(donor_list, True, True,
                                         currency_symbol, 1)
    text2 = extralife_IO.multiple_format(donor_list, True, True,
                                         currency_symbol, 2)
    text3 = extralife_IO.multiple_format(donor_list,                                   True, True, currency_symbol, 3)
    text4 = extralife_IO.multiple_format(donor_list, True, True,
                                         currency_symbol, 4)
    text5 = extralife_IO.multiple_format(donor_list, True, True,
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
    donor1 = donation.Donation("donor1", "message1", 10)
    donor2 = donation.Donation("donor2", "message2", 20)
    donor3 = donation.Donation("donor3", "message3", 30)
    donor4 = donation.Donation("donor4", "message4", 40)
    donor5 = donation.Donation("donor5", "message5", 50)
    donor6 = donation.Donation("donor6", "message6", 60)
    donor_list = [donor1, donor2, donor3, donor4, donor5, donor6]
    currency_symbol = "$"
    text1 = extralife_IO.multiple_format(donor_list, False, False,
                                         currency_symbol, 1)
    text2 = extralife_IO.multiple_format(donor_list, False, False,
                                         currency_symbol, 2)
    text3 = extralife_IO.multiple_format(donor_list,                                   False, False, currency_symbol, 3)
    text4 = extralife_IO.multiple_format(donor_list, False, False,
                                         currency_symbol, 4)
    text5 = extralife_IO.multiple_format(donor_list, False, False,
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
    donor1 = donation.Donation("donor1", "message1", 10)
    donor2 = donation.Donation("donor2", "message2", 20)
    donor3 = donation.Donation("donor3", "message3", 30)
    donor4 = donation.Donation("donor4", "message4", 40)
    donor5 = donation.Donation("donor5", "message5", 50)
    donor6 = donation.Donation("donor6", "message6", 60)
    donor_list = [donor1, donor2, donor3, donor4, donor5, donor6]
    currency_symbol = "$"
    text1 = extralife_IO.multiple_format(donor_list, True, False,
                                         currency_symbol, 1)
    text2 = extralife_IO.multiple_format(donor_list, True, False,
                                         currency_symbol, 2)
    text3 = extralife_IO.multiple_format(donor_list,                                   True, False, currency_symbol, 3)
    text4 = extralife_IO.multiple_format(donor_list, True, False,
                                         currency_symbol, 4)
    text5 = extralife_IO.multiple_format(donor_list, True, False,
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
    extralife_IO.write_text_files(dictionary, text_folder)
    with open(f"testOutput/testfilename.txt") as file:
        fileinput = file.read()
    assert fileinput == "test output"


def test_write_text_files_unicode():
    """ Test that unicode gets written to the text files correctly. """
    fileinput = ""
    dictionary = {"testfilename": "áéíóúñ"}
    text_folder = "testOutput"
    extralife_IO.write_text_files(dictionary, text_folder)
    with open(f"testOutput/testfilename.txt", 'r', encoding='utf8') as file:
        fileinput = file.read()
    assert fileinput == "áéíóúñ"


def test_write_text_files_emoji():
    """ Test that emojis get written to the text files correctly. """
    fileinput = ""
    dictionary = {"testfilename": "😁😂🧐🙏🚣🌸🦞🏰💌"}
    text_folder = "testOutput"
    extralife_IO.write_text_files(dictionary, text_folder)
    with open(f"testOutput/testfilename.txt", 'r', encoding='utf8') as file:
        fileinput = file.read()
    assert fileinput == "😁😂🧐🙏🚣🌸🦞🏰💌"
