from unittest import mock

from eldonationtracker.participant import Participant
import eldonationtracker.participant

config = ("12345", "textfolder", "$", "45678", "5")
fake_participant_conf = mock.Mock()
fake_participant_conf.get_CLI_values.return_value = config

config_no_team = ("12345", "textfolder", "$", None, "5")
fake_participant_conf_no_team = mock.Mock()
fake_participant_conf_no_team.get_CLI_values.return_value = config_no_team

fake_participant_info = {'sumDonations': 500, 'numDonations': 5, 'fundraisingGoal': 1000}
fake_donations = {"displayName": "Sean Gibson", "participantID": 401280, "amount": 25.00, "donorID":"54483486D840B7EA",
                  "avatarImageURL": "//assets.donordrive.com/clients/extralife/img/avatar-constituent-default.gif",
                  "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                  "donationID": "861A3C59D235B4DA"}, {"displayName": "Eric Mesa", "participantID": 401280,
                                                      "amount": 25.00, "donorID": "4162ECD2B8BF4C17",
                                                      "avatarImageURL": "//assets.donordrive.com/extralife/images/$avat"
                                                                        "ars$/constituent_D4DC394A-C293-34EB-4162ECD2B"
                                                                        "8BF4C17.jpg",
                                                      "createdDateUTC": "2020-01-05T20:35:28.897+0000",
                                                      "eventID": 547, "teamID": 50394, "donationID": "7D430E9E9AF79686"}
fake_extralife_io = mock.Mock()
fake_extralife_io.get_JSON.return_value = fake_participant_info
fake_extralife_io.get_JSON_donations.return_value = fake_donations
fake_extralife_io.get_JSON_no_json.return_value = {}
fake_extralife_io.get_JSON_donations_no_json.return_value = {}

def test_api_variables():
    my_participant = Participant(fake_participant_conf)
    assert (my_participant.ExtraLifeID, my_participant.textFolder,
            my_participant.CurrencySymbol, my_participant.TeamID,
            my_participant.donors_to_display) == ("12345", "textfolder", "$", "45678", "5")


def test_urls():
    my_participant = Participant(fake_participant_conf)
    assert my_participant.participant_url == "https://www.extra-life.org/api/participants/12345"
    assert my_participant.donation_url == "https://www.extra-life.org/api/participants/12345/donations"
    assert my_participant.participant_donor_URL == "https://www.extra-life.org/api/participants/12345/donors"


def test_str_with_a_team():
    my_participant = Participant(fake_participant_conf)
    assert str(my_participant) == "A participant with Extra Life ID 12345. Team info: A team found at https://www.extra-life.org/api/teams/45678 ."


def test_str_without_a_team():
    my_participant = Participant(fake_participant_conf_no_team)
    assert str(my_participant) == "A participant with Extra Life ID 12345. Team info: Not a valid team - no team_id."


@mock.patch.object(eldonationtracker.participant.extralife_io, "get_JSON", fake_extralife_io.get_JSON)
def test_get_participant_info():
    my_participant = Participant(fake_participant_conf)
    assert my_participant._get_participant_info() == (500, 5, 1000)


@mock.patch.object(eldonationtracker.participant.extralife_io, "get_JSON", fake_extralife_io.get_JSON_no_json)
def test_get_participant_info_no_json():
    my_participant = Participant(fake_participant_conf)
    assert my_participant._get_participant_info() == (0, 0, 0)


def test_format_participant_info_for_output():
    my_participant = Participant(fake_participant_conf)
    my_participant.total_raised = 400
    my_participant.average_donation = 100
    my_participant.goal = 1000
    assert my_participant._format_participant_info_for_output(my_participant.total_raised) == "$400.00"
    assert my_participant._format_participant_info_for_output(my_participant.average_donation) == "$100.00"
    assert my_participant._format_participant_info_for_output(my_participant.goal) == "$1,000.00"


def test_fill_participant_dictionary():
    my_participant = Participant(fake_participant_conf)
    my_participant.total_raised = 400
    my_participant.average_donation = 100
    my_participant.goal = 1000
    my_participant._fill_participant_dictionary()
    assert my_participant.participant_formatted_output["totalRaised"] == "$400.00"
    assert my_participant.participant_formatted_output["averageDonation"] == "$100.00"
    assert my_participant.participant_formatted_output["goal"] == "$1,000.00"


def test_calculate_average_donation():
    my_participant = Participant(fake_participant_conf)
    my_participant.total_raised = 100
    my_participant.number_of_donations = 2
    assert my_participant._calculate_average_donation() == 50


def test_calculate_average_donation_no_donations():
    my_participant = Participant(fake_participant_conf)
    my_participant.total_raised = 0
    my_participant.number_of_donations = 0
    assert my_participant._calculate_average_donation() == 0


@mock.patch.object(eldonationtracker.participant.extralife_io, "get_JSON", fake_extralife_io.get_JSON_donations)
def test_get_donations():
    my_participant = Participant(fake_participant_conf)
    my_participant.donation_list = my_participant._get_donations(my_participant.donation_list)
    assert my_participant.donation_list[0].name == "Sean Gibson"
    assert my_participant.donation_list[1].name == "Eric Mesa"


@mock.patch.object(eldonationtracker.participant.extralife_io, "get_JSON", fake_extralife_io.get_JSON_donations_no_json)
def test_get_donations_no_json():
    my_participant = Participant(fake_participant_conf)
    my_participant.donation_list = my_participant._get_donations(my_participant.donation_list)
    assert my_participant.donation_list == []


@mock.patch.object(eldonationtracker.participant.extralife_io, "get_JSON", fake_extralife_io.get_JSON_donations)
def test_get_donations_already_a_donation_present():
    my_participant = Participant(fake_participant_conf)
    donation1 = eldonationtracker.participant.donation.Donation("Donor 1", "Good job!", 34.51, "4939d",
                                                                "http://image.png",
                                                                "2020-02-11T17:22:23.963+0000", "fakedonationid")
    my_participant.donation_list = [donation1]
    my_participant.donation_list = my_participant._get_donations(my_participant.donation_list)
    print(my_participant.donation_list)
    assert my_participant.donation_list[0].name == "Sean Gibson"
    assert my_participant.donation_list[1].name == "Eric Mesa"
    assert my_participant.donation_list[2].name == "Donor 1"

# tests to do:
# _get_top_donor
# _format_donor_information_for_output
# _format_donation_information_for_output
# write_text_files? Or don't test?
# the "loop" itself
