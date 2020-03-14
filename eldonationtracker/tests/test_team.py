"""Unit tests for team.py."""

from eldonationtracker import team as team


def test_team_url():
    my_team = team.Team("12345", "folder", "$")
    assert my_team.team_url == "https://www.extra-life.org/api/teams/12345"


def test_team_participant_url():
    my_team = team.Team("12345", "folder", "$")
    assert my_team.team_participant_url == "https://www.extra-life.org/api/teams/12345/participants"
