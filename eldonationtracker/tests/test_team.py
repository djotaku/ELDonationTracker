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
