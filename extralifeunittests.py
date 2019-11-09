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
