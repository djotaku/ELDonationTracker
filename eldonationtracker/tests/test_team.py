"""Unit tests for team.py."""

from unittest import mock

from eldonationtracker import team as team


def test_team_url():
    my_team = team.Team("12345", "folder", "$")
    assert my_team.team_url == "https://www.extra-life.org/api/teams/12345"


def test_team_participant_url():
    my_team = team.Team("12345", "folder", "$")
    assert my_team.team_participant_url == "https://www.extra-life.org/api/teams/12345/participants"


def test_get_team_json():
    with mock.patch("eldonationtracker.team.extralife_io.get_json",
                    return_value={"fundraisingGoal": 500, "captainDisplayName": "Captain Awesome",
                                  "sumDonations": 400, "numDonations": 300}):
        my_team = team.Team("12345", "folder", "$")
        team_json = my_team._get_team_json()
        assert team_json == (500, 'Captain Awesome', 400, 300)


def test_get_team_json_no_json():
    with mock.patch("eldonationtracker.team.extralife_io.get_json", return_value={}):
        my_team = team.Team("12345", "folder", "$")
        team_json = my_team._get_team_json()
        assert team_json == (0, '', 0, 0)
        # let's pretend that at some point values were added
        # but now the API can't be reached. Let's make sure it doesn't over-write the good data.
        my_team.team_goal = 500
        my_team.team_captain = 'Captain Awesome'
        my_team.total_raised = 400
        my_team.num_donations = 300
        team_json = my_team._get_team_json()
        assert team_json == (500, 'Captain Awesome', 400, 300)


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
