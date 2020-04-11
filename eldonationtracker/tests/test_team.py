"""Unit tests for team.py."""

from eldonationtracker import team as team


def test_team_url():
    my_team = team.Team("12345", "folder", "$")
    assert my_team.team_url == "https://www.extra-life.org/api/teams/12345"


def test_team_participant_url():
    my_team = team.Team("12345", "folder", "$")
    assert my_team.team_participant_url == "https://www.extra-life.org/api/teams/12345/participants"


def test_str_no_json_data():
    """Test what str will produce if the JSON retrieval hasn't yet run."""
    my_team = team.Team("12345", "folder", "$")
    assert str(my_team) == "A team found at https://www.extra-life.org/api/teams/12345 ."


def test_str_no_json_data_no_team_id():
    """Test what str will produce if the JSON retrieval hasn't yet run AND no team ID.

    This would happen if the user is not part of a team.
    """
    my_team = team.Team(None, "folder", "$")
    assert str(my_team) == "Not a valid team - no team_id."


def test_TeamParticipant_str():
    team_donor1_json = {"displayName": "donor1", "sumDonations": "45", "donorID": 1000111,
                        'avatarImageURL': "http://someplace.com/image.jpg", "numDonations": 2}
    team_donor1 = team.TeamParticipant(team_donor1_json)
    assert str(team_donor1) == "A Team Participant named donor1 who has donated $45.00 to the team over 2 donations."
