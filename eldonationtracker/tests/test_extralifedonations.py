from unittest import mock

import eldonationtracker.extralifedonations as participant

config = ("12345", "textfolder", "$", "45678", "5")
fake_participant_conf = mock.Mock()
fake_participant_conf.get_CLI_values.return_value = config

config_no_team = ("12345", "textfolder", "$", None, "5")
fake_participant_conf_no_team = mock.Mock()
fake_participant_conf_no_team.get_CLI_values.return_value = config_no_team


def test_api_variables():
    my_participant = participant.Participant(fake_participant_conf)
    assert (my_participant.ExtraLifeID, my_participant.textFolder,
            my_participant.CurrencySymbol, my_participant.TeamID,
            my_participant.donors_to_display) == ("12345", "textfolder", "$", "45678", "5")


def test_participant_url():
    my_participant = participant.Participant(fake_participant_conf)
    assert my_participant.participant_url == "https://www.extra-life.org/api/participants/12345"


def test_donor_url():
    my_participant = participant.Participant(fake_participant_conf)
    assert my_participant.donation_url == "https://www.extra-life.org/api/participants/12345/donations"


def test_participant_donor_url():
    my_participant = participant.Participant(fake_participant_conf)
    assert my_participant.participant_donor_URL == "https://www.extra-life.org/api/participants/12345/donors"


def test_str_with_a_team():
    my_participant = participant.Participant(fake_participant_conf)
    assert str(my_participant) == "A participant with Extra Life ID 12345. Team info: A team found at https://www.extra-life.org/api/teams/45678 ."


def test_str_without_a_team():
    my_participant = participant.Participant(fake_participant_conf_no_team)
    assert str(my_participant) == "A participant with Extra Life ID 12345. Team info: Not a valid team - no team_id."

