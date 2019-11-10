import extralifedonations

# run with command: py.test-3 extralifeunittests.py
# or if in venv, just pytest extralifeunittests.py (works better)


# Tests for class Donor
def test_Donor_lt():
    """ Test to make sure comparison works. """
    donor1 = extralifedonations.Donor("donor1", "message", 45)
    donor2 = extralifedonations.Donor("donor2", "message", 30)
    assert donor2 < donor1


# Tests for class Participant
# Come back and develop tests for get_participant_JSON and 
# get_donors after changing the methods to take input
# and return a value. That will be in prep for refactoring.
def test_donor_formatting_message_true():
    """ Make sure the formatting works correctly. """
    p = extralifedonations.Participant()
    donor1 = extralifedonations.Donor("donor1", "message", 45)
    formatted_message = p._donor_formatting(donor1, True)
    assert formatted_message == "donor1 - $45.00 - message"


def test_donor_formatting_message_false():
    """ Make sure the formatting works correctly. """
    p = extralifedonations.Participant()
    donor1 = extralifedonations.Donor("donor1", "message", 45)
    formatted_message = p._donor_formatting(donor1, False)
    assert formatted_message == "donor1 - $45.00"


def test_last5donors_Horizontal():
    """ Does it return the right thing? 

    I include an extra donor to make sure it stops at 5."""
    donor1 = extralifedonations.Donor("donor1", "message1", 10)
    donor2 = extralifedonations.Donor("donor2", "message2", 20)
    donor3 = extralifedonations.Donor("donor3", "message3", 30)
    donor4 = extralifedonations.Donor("donor4", "message4", 40)
    donor5 = extralifedonations.Donor("donor5", "message5", 50)
    donor6 = extralifedonations.Donor("donor6", "message6", 60)
    donor_list = [donor1, donor2, donor3, donor4, donor5, donor6]
    p = extralifedonations.Participant()
    text = p._last5donors(donor_list, False, True)
    assert text == "donor1 - $10.00 | donor2 - $20.00 | donor3 - $30.00 | donor4 - $40.00 | donor5 - $50.00 | "


def test_last5donors_Message_Horizontal():
    """ Does it return the right thing? 

    I include an extra donor to make sure it stops at 5."""
    donor1 = extralifedonations.Donor("donor1", "message1", 10)
    donor2 = extralifedonations.Donor("donor2", "message2", 20)
    donor3 = extralifedonations.Donor("donor3", "message3", 30)
    donor4 = extralifedonations.Donor("donor4", "message4", 40)
    donor5 = extralifedonations.Donor("donor5", "message5", 50)
    donor6 = extralifedonations.Donor("donor6", "message6", 60)
    donor_list = [donor1, donor2, donor3, donor4, donor5, donor6]
    p = extralifedonations.Participant()
    text = p._last5donors(donor_list, True, True)
    assert text == "donor1 - $10.00 - message1 | donor2 - $20.00 - message2 | donor3 - $30.00 - message3 | donor4 - $40.00 - message4 | donor5 - $50.00 - message5 | "


def test_last5donors_Vertical():
    """ Does it return the right thing? 

    I include an extra donor to make sure it stops at 5."""
    donor1 = extralifedonations.Donor("donor1", "message1", 10)
    donor2 = extralifedonations.Donor("donor2", "message2", 20)
    donor3 = extralifedonations.Donor("donor3", "message3", 30)
    donor4 = extralifedonations.Donor("donor4", "message4", 40)
    donor5 = extralifedonations.Donor("donor5", "message5", 50)
    donor6 = extralifedonations.Donor("donor6", "message6", 60)
    donor_list = [donor1, donor2, donor3, donor4, donor5, donor6]
    p = extralifedonations.Participant()
    text = p._last5donors(donor_list, False, False)
    assert text == "donor1 - $10.00\ndonor2 - $20.00\ndonor3 - $30.00\ndonor4 - $40.00\ndonor5 - $50.00\n"


def test_last5donors_Message_Vertical():
    """ Does it return the right thing? 

    I include an extra donor to make sure it stops at 5."""
    donor1 = extralifedonations.Donor("donor1", "message1", 10)
    donor2 = extralifedonations.Donor("donor2", "message2", 20)
    donor3 = extralifedonations.Donor("donor3", "message3", 30)
    donor4 = extralifedonations.Donor("donor4", "message4", 40)
    donor5 = extralifedonations.Donor("donor5", "message5", 50)
    donor6 = extralifedonations.Donor("donor6", "message6", 60)
    donor_list = [donor1, donor2, donor3, donor4, donor5, donor6]
    p = extralifedonations.Participant()
    text = p._last5donors(donor_list, True, False)
    assert text == "donor1 - $10.00 - message1\ndonor2 - $20.00 - message2\ndonor3 - $30.00 - message3\ndonor4 - $40.00 - message4\ndonor5 - $50.00 - message5\n"


def test_donor_calculations():
    """ Since _donor_calculations is just using the two methods I tested above I'm going to assume it is correct unless someone points out why it still needs a unit test."""
    pass


def test_write_text_files():
    """ Test that data gets written to the text files correctly. """
    fileinput = ""
    dictionary = {"testfilename": "test output"}
    p = extralifedonations.Participant()
    p.textFolder = "testOutput"
    p.write_text_files(dictionary)
    with open(f"testOutput/testfilename.txt") as file:
        fileinput = file.read()
    assert fileinput == "test output"


def test_write_text_files_unicode():
    """ Test that unicode gets written to the text files correctly. """
    fileinput = ""
    dictionary = {"testfilename": "áéíóúñ"}
    p = extralifedonations.Participant()
    p.textFolder = "testOutput"
    p.write_text_files(dictionary)
    with open(f"testOutput/testfilename.txt") as file:
        fileinput = file.read()
    assert fileinput == "áéíóúñ"


def test_write_text_files_emoji():
    """ Test that emojis get written to the text files correctly. """
    fileinput = ""
    dictionary = {"testfilename": "😁😂🧐🙏🚣🌸🦞🏰💌"}
    p = extralifedonations.Participant()
    p.textFolder = "testOutput"
    p.write_text_files(dictionary)
    with open(f"testOutput/testfilename.txt") as file:
        fileinput = file.read()
    assert fileinput == "😁😂🧐🙏🚣🌸🦞🏰💌"


# Tests for Class Team
# skipping JSON for now since I'm going to refactor that output
# in fact, nearly everything here is a variant of participant
# and will get refactored out.

# Tests for IPC.py
# Don't see a need to test anything here as it's the most
# basic of functions.

# Tests for readparticipantconf.py
# right now not sure what tests I need here
