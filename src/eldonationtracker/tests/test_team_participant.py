"""Unit tests for team_participant.py"""

import eldonationtracker.api.team_participant


def test_team_participant_str():
    team_donor1_json = {"displayName": "donor1", "sumDonations": "45", "donorID": 1000111,
                        'avatarImageURL': "http://someplace.com/image.jpg", "numDonations": 2}
    team_donor1 = eldonationtracker.api.team_participant.TeamParticipant(team_donor1_json)
    assert str(team_donor1) == "A Team Participant named donor1 who has donated $45.00 to the team over 2 donations."


def test_team_participant_str_no_donor_name():
    team_donor1_json = {"sumDonations": "45", "donorID": 1000111,
                        'avatarImageURL': "http://someplace.com/image.jpg", "numDonations": 2}
    team_donor1 = eldonationtracker.api.team_participant.TeamParticipant(team_donor1_json)
    assert str(team_donor1) == "A Team Participant named Anonymous who has donated $45.00 to the team over 2 donations."
