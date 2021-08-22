# type: ignore

import json
from unittest import mock

from eldonationtracker.api.participant import Participant, Milestone
import eldonationtracker.api.participant
from eldonationtracker.api.badge import Badge

config = ("12345", "textfolder", "$", "45678", "5")
fake_participant_conf = mock.Mock()
fake_participant_conf.get_cli_values.return_value = config

config_no_team = ("12345", "textfolder", "$", None, "5")
fake_participant_conf_no_team = mock.Mock()
fake_participant_conf_no_team.get_cli_values.return_value = config_no_team

fake_participant_info = {"displayName": "Eric Mesa", "fundraisingGoal": 600.00, "participantID": 449263.0,
                         "eventName": "Extra Life 2021", "teamName": "Twitchclub", "isTeamCaptain": False,
                         "avatarImageURL": "//assets.donordrive.com/extralife/images/$avatars$/constituent_D4DC394A-C293-34EB-4162ECD2B8BF4C17.jpg",
                         "streamIsLive": False,
                         "links":
                             {"donate":
                                  "https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=449263#donate",
                              "stream": "https://player.twitch.tv/?channel=djotaku",
                              "page":
                                  "https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=449263"},
                         "createdDateUTC": "2021-01-03T21:45:29.523+0000", "eventID": 550.0, "sumDonations": 75.00,
                         "sumPledges": 0.00, "numDonations": 2.0}
fake_participant_info_no_team = {"displayName": "Eric Mesa", "fundraisingGoal": 600.00, "participantID": 449263.0,
                                 "eventName": "Extra Life 2021",
                                 "avatarImageURL": "//assets.donordrive.com/extralife/images/$avatars$/constituent_D4DC394A-C293-34EB-4162ECD2B8BF4C17.jpg",
                                 "streamIsLive": False,
                                 "links":
                                 {"donate":
                                  "https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=449263#donate",
                                  "stream": "https://player.twitch.tv/?channel=djotaku",
                                  "page":
                                   "https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=449263"},
                                 "createdDateUTC": "2021-01-03T21:45:29.523+0000", "eventID": 550.0,
                                 "sumDonations": 75.00, "sumPledges": 0.00, "numDonations": 2.0}

fake_donations = {"displayName": "Sean Gibson", "participantID": 401280, "amount": 25.00, "donorID": "54483486D840B7EA",
                  "avatarImageURL": "//assets.donordrive.com/clients/extralife/img/avatar-constituent-default.gif",
                  "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                  "donationID": "861A3C59D235B4DA"}, {"displayName": "Eric Mesa", "participantID": 401280,
                                                      "amount": 25.00, "donorID": "4162ECD2B8BF4C17",
                                                      "avatarImageURL": "//assets.donordrive.com/extralife/images/$avat"
                                                                        "ars$/constituent_D4DC394A-C293-34EB-4162ECD2B"
                                                                        "8BF4C17.jpg",
                                                      "createdDateUTC": "2020-01-05T20:35:28.897+0000",
                                                      "eventID": 547, "teamID": 50394, "donationID": "7D430E9E9AF79686"}

donor1_json = {"displayName": "donor1", "sumDonations": "45", "donorID": 1000111,
               'avatarImageURL': "http://someplace.com/image.jpg", "numDonations": 2}
donor2_json = {"displayName": "donor2", "sumDonations": "20", "donorID": 1000112,
               'avatarImageURL': "http://someplace.com/image.jpg", "numDonations": 3}
donor1 = eldonationtracker.api.donor.Donor(donor1_json)
donor2 = eldonationtracker.api.donor.Donor(donor2_json)
fake_top_donor_json = [{"displayName": "Top Donor", "sumDonations": "100", "donorID": 1000111,
                       'avatarImageURL': "http://someplace.com/image.jpg", "numDonations": 2}]

donation1_json = {"displayName": "Donor 1", "participantID": '4939d', "amount": 34.51, "donorID": "FAKE3C59D235B4DA",
                  "avatarImageURL": "//image.png", "message": "Good job! From Donor 1",
                  "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                  "donationID": "861A3C59D235B4DA"}
donation2_json = {"displayName": "Donor 2", "participantID": '4939d', "amount": 34.51, "donorID": "FAKE3C59D235B4DA",
                  "avatarImageURL": "//image.png",
                  "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                  "donationID": "861A3C59D235B4DB"}
donation_anonymous_json = {"displayName": None, "participantID": '4939d', "amount": 34.51,
                           "donorID": "FAKE3C59D235B4DA", "avatarImageURL": "//image.png",
                           "message": "Good job! From Donor 3",
                           "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                           "donationID": "861A3C59D235B4DC"}


fake_extralife_io = mock.Mock()
fake_extralife_io.get_json.return_value = fake_participant_info
fake_extralife_io.get_JSON_donations.return_value = fake_donations
fake_extralife_io.get_JSON_no_json.return_value = {}
fake_extralife_io.get_JSON_donations_no_json.return_value = {}
fake_extralife_io.get_JSON_top_donor_no_json.return_value = {}
fake_extralife_io.get_json_no_team.return_value = fake_participant_info_no_team

magic_fake_extralife_io = mock.MagicMock()
magic_fake_extralife_io.get_JSON_top_donor.return_value = fake_top_donor_json

fake_participant = mock.Mock()
fake_participant.write_text_files.return_value = None
fake_participant._format_donation_information_for_output.return_value = None
fake_participant._format_donor_information_for_output.return_value = None

fake_participant_for_run = mock.Mock()
fake_participant_for_run.update_participant_attributes.return_value = None
fake_participant_for_run.output_participant_data.return_value = None
fake_participant_for_run.write_ipc.return_value = None
fake_participant_for_run.update_donation_data.return_value = None
fake_participant_for_run.output_donation_data.return_value = None
fake_participant_for_run.update_donor_data.return_value = None
fake_participant_for_run.output_donor_data.return_value = None
fake_participant_for_run._update_milestones.return_value = None
fake_participant_for_run.output_milestone_data.return_value = None
fake_participant_for_run.my_team.team_run.return_value = None
fake_participant_for_run.my_team.participant_run.return_value = None
fake_participant_for_run._update_incentives.return_value = None
fake_participant_for_run.output_incentive_data.return_value = None


def test_api_variables():
    """Test that API variables are properly assigned."""
    my_participant = Participant(fake_participant_conf)
    assert (my_participant.extralife_id, my_participant.text_folder,
            my_participant.currency_symbol, my_participant.team_id,
            my_participant.donors_to_display) == ("12345", "textfolder", "$", "45678", "5")


def test_urls():
    """Make sure the API URLs are properly constructed."""
    my_participant = Participant(fake_participant_conf)
    assert my_participant.participant_url == "https://www.extra-life.org/api/participants/12345"
    assert my_participant.donation_url == "https://www.extra-life.org/api/participants/12345/donations"
    assert my_participant.participant_donor_url == "https://www.extra-life.org/api/participants/12345/donors"


def test_str_with_a_team():
    """Test the str(participant) string if the participant is part of a team."""
    my_participant = Participant(fake_participant_conf)
    assert str(my_participant) == "A participant with Extra Life ID 12345. Team info: A team found at https://www.extra-life.org/api/teams/45678. "


def test_str_without_a_team():
    """Test the str(participant) string if the participant is not part of a team."""
    my_participant = Participant(fake_participant_conf_no_team)
    assert str(my_participant) == "A participant with Extra Life ID 12345."


def test_new_donation_property():
    """Test that new donation property and setter are working correctly."""
    my_participant = Participant(fake_participant_conf_no_team)
    assert my_participant.new_donation is False
    my_participant.new_donation = True
    assert my_participant.new_donation


@mock.patch.object(eldonationtracker.utils.extralife_io, "get_json", fake_extralife_io.get_json)
def test_get_participant_info():
    """Make sure the API info for the participant is properly assigned."""
    my_participant = Participant(fake_participant_conf)
    assert my_participant._get_participant_info() == (75.0, 2, 600, "//assets.donordrive.com/extralife/images/$avatars$/constituent_D4DC394A-C293-34EB-4162ECD2B8BF4C17.jpg",
                                                      'Extra Life 2021', 'https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=449263#donate',
                                                      'https://player.twitch.tv/?channel=djotaku',
                                                      'https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=449263',
                                                      '2021-01-03T21:45:29.523+0000', False, 0, 'Twitchclub', False,
                                                      'Eric Mesa')


@mock.patch.object(eldonationtracker.utils.extralife_io, "get_json", fake_extralife_io.get_json_no_team)
def test_get_participant_info_no_team():
    """Make sure the API info for the participant is properly assigned."""
    my_participant = Participant(fake_participant_conf)
    my_participant._my_team = None
    assert my_participant._get_participant_info() == (75.0, 2, 600, "//assets.donordrive.com/extralife/images/$avatars$/constituent_D4DC394A-C293-34EB-4162ECD2B8BF4C17.jpg",
                                                      'Extra Life 2021', 'https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=449263#donate',
                                                      'https://player.twitch.tv/?channel=djotaku',
                                                      'https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=449263',
                                                      '2021-01-03T21:45:29.523+0000', False, 0, '', False,
                                                      'Eric Mesa')


@mock.patch.object(eldonationtracker.utils.extralife_io, "get_json", fake_extralife_io.get_JSON_no_json)
def test_get_participant_info_no_json():
    """Ensure that the proper values are returned if the JSON values are not retrieved from the API."""
    my_participant = Participant(fake_participant_conf)
    assert my_participant._get_participant_info() == (0, 0, 0, '', '', '', '', '', '', False, 0, '', False, '')


def test_format_participant_info_for_output():
    """Make sure the right values are grabbed from the participant properties."""
    my_participant = Participant(fake_participant_conf)
    my_participant._total_raised = 400
    my_participant._average_donation = 100
    my_participant._goal = 1000
    assert my_participant._format_participant_info_for_output(my_participant.total_raised) == "$400.00"
    assert my_participant._format_participant_info_for_output(my_participant.average_donation) == "$100.00"
    assert my_participant._format_participant_info_for_output(my_participant.goal) == "$1,000.00"


def test_fill_participant_dictionary():
    """Make sure the output formatted dictionary has the right info."""
    my_participant = Participant(fake_participant_conf)
    my_participant._total_raised = 400
    my_participant._average_donation = 100
    my_participant._goal = 1000
    my_participant._fill_participant_dictionary()
    assert my_participant._participant_formatted_output["totalRaised"] == "$400.00"
    assert my_participant._participant_formatted_output["averageDonation"] == "$100.00"
    assert my_participant._participant_formatted_output["goal"] == "$1,000.00"


def test_calculate_average_donation():
    """Make sure the average donation is properly calculated."""
    my_participant = Participant(fake_participant_conf)
    my_participant._total_raised = 100
    my_participant._number_of_donations = 2
    assert my_participant._calculate_average_donation() == 50


def test_calculate_average_donation_no_donations():
    """Make sure the average donation is properly calculated if there haven't been any donations yet."""
    my_participant = Participant(fake_participant_conf)
    my_participant._total_raised = 0
    my_participant._number_of_donations = 0
    assert my_participant._calculate_average_donation() == 0


@mock.patch.object(eldonationtracker.utils.extralife_io, "get_json", fake_extralife_io.get_JSON_top_donor_no_json)
def test_get_top_donor_no_json():
    """Make sure the top donor works correctly if the JSON was not returned."""
    my_participant = Participant(fake_participant_conf)
    my_participant._top_donor = donor1
    my_participant.update_donor_data()
    assert my_participant._top_donor == donor1


def test_format_donor_information_for_output():
    """Make sure the donor information is properly formatted for the users."""
    my_participant = Participant(fake_participant_conf)
    my_participant._top_donor = donor1
    my_participant._donor_list = [donor2, donor1]
    my_participant._format_donor_information_for_output()
    assert my_participant._top_donor_formatted_output['TopDonorNameAmnt'] == "donor1 - $45.00"
    assert my_participant._donor_formatted_output['LastDonorNameAmnt'] == "donor2 - $20.00"
    assert my_participant._donor_formatted_output['lastNDonorNameAmts'] == "donor2 - $20.00\ndonor1 - $45.00\n"


def test_format_donation_information_for_output():
    """Test donation output for the users."""
    my_participant = Participant(fake_participant_conf)
    donation1 = eldonationtracker.api.donation.Donation(donation1_json)
    donation2 = eldonationtracker.api.donation.Donation(donation2_json)
    donation3 = eldonationtracker.api.donation.Donation(donation_anonymous_json)
    my_participant._donation_list = [donation3, donation2, donation1]
    my_participant._top_donation = donation1
    my_participant._format_donation_information_for_output()
    assert my_participant._donation_formatted_output['LastDonationNameAmnt'] == "Anonymous - $34.51"
    assert my_participant._donation_formatted_output['lastNDonationNameAmts'] == "Anonymous - $34.51\nDonor 2 - $34.51" \
                                                                                "\nDonor 1 - $34.51\n"
    assert my_participant._donation_formatted_output['lastNDonationNameAmtsMessage'] == "Anonymous - $34.51 - Good job" \
                                                                                       "! From Donor 3\nDonor 2 - $34" \
                                                                                       ".51 - None\nDonor 1 - $34.51" \
                                                                                       " - Good job! From Donor 1\n"
    assert my_participant._donation_formatted_output['lastNDonationNameAmtsMessageHorizontal'] == "Anonymous - $34.51" \
                                                                                                 " - Good job! From " \
                                                                                                 "Donor 3 | Donor 2 -" \
                                                                                                 " $34.51 - None | " \
                                                                                                 "Donor 1 - $34.51 - " \
                                                                                                 "Good job! From " \
                                                                                                 "Donor 1 | "
    assert my_participant._donation_formatted_output['lastNDonationNameAmtsHorizontal'] == "Anonymous - $34.51" \
                                                                                          " | Donor 2 - $34.51" \
                                                                                          " | Donor 1 - $34.51 | "


def test_update_donation_data_no_donations():
    """Make sure the donation data is updated correctly if there are no donations."""
    my_participant = Participant(fake_participant_conf)
    my_participant.update_donation_data()
    assert my_participant._donation_list == []


@mock.patch.object(eldonationtracker.utils.extralife_io, "get_json", fake_extralife_io.get_JSON_donations)
def test_update_donation_data_preexisting_donations():
    my_participant = Participant(fake_participant_conf)
    my_participant._number_of_donations = 2
    my_participant.update_donation_data()
    assert my_participant._donation_list[0].name == "Sean Gibson"


def test_update_donor_data_no_donations():
    my_participant = Participant(fake_participant_conf)
    my_participant.update_donor_data()
    assert my_participant._top_donor is None


magic_fake_extralife_io_donor = mock.MagicMock()
magic_fake_extralife_io_donor.get_donors.return_value = [donor1]


@mock.patch.object(eldonationtracker.utils.extralife_io, "get_donations", magic_fake_extralife_io_donor.get_donors)
def test_update_donor_data():
    my_participant = Participant(fake_participant_conf)
    my_participant._number_of_donations = 2
    my_participant.update_donor_data()
    assert my_participant._top_donor.name == "donor1"


example_json = """[
    {
        "description": "Raised 100 dollars!",
        "title": "100 Club Badge",
        "unlockedDateUTC": "2019-10-30T18:01:23.430+0000",
        "badgeImageURL": "http://assets.donordrive.com/try/images/$event508$/badge_2F7819D3_C019_3C7D_B9D716687CEEC0A5.png",
        "badgeCode": "100-club-badge"
      },
      {
        "description": "Sent 25 donation invite emails!",
        "title": "Enthusiastic Participant Badge",
        "unlockedDateUTC": "2019-09-18T15:47:39.107+0000",
        "badgeImageURL": "https://assets.donordrive.com/try/images/$event508$/badge_DCB0A883_BC0A_97DB_639B4D7BFDEC638E.png",
        "badgeCode": "enthusiastic-participant-badge"
      }
    ]"""
example_json_as_json = json.loads(example_json)
test_badges = [Badge.create_badge(a_badge) for a_badge in example_json_as_json]
magic_fake_badges = mock.MagicMock()
magic_fake_badges.get_badges.return_value = test_badges


@mock.patch.object(eldonationtracker.utils.extralife_io, "get_badges", magic_fake_badges.get_badges)
def test_update_badges():
    """Test to make sure that badges are updated."""
    my_participant = Participant(fake_participant_conf)
    assert my_participant.badges == []
    my_participant._update_badges()
    assert my_participant.badges[0].badge_code == "100-club-badge"


magic_fake_milestones = mock.MagicMock()
magic_fake_milestones.get_milestones.return_value = "something"

# note: order matters - this one needs to go before the one where _format_donation...output is called or the not called
# fails.
@mock.patch.object(eldonationtracker.api.participant.Participant, 'write_text_files', fake_participant.write_text_files)
@mock.patch.object(eldonationtracker.api.participant.Participant, '_format_donation_information_for_output',
                   fake_participant._format_donation_information_for_output)
def test_output_donation_data_no_donations():
    my_participant = Participant(fake_participant_conf)
    my_participant.output_donation_data()
    assert my_participant._donation_list == []
    fake_participant._format_donation_information_for_output.assert_not_called()
    fake_participant.write_text_files.assert_called()


donation_for_output_json = {"displayName": "Donor 1", "participantID": '4939d', "amount": 34.51,
                            "donorID": "FAKE3C59D235B4DA", "avatarImageURL": "//image.png", "message": "Good job!",
                            "createdDateUTC": "2020-02-11T17:22:23.963+0000", "eventID": 547, "teamID": 50394,
                            "donationID": "861A3C59D235B4DB"}
donation_for_output = eldonationtracker.api.donation.Donation(donation1_json)


@mock.patch.object(eldonationtracker.api.participant.Participant, 'write_text_files', fake_participant.write_text_files)
@mock.patch.object(eldonationtracker.api.participant.Participant, '_format_donation_information_for_output',
                   fake_participant._format_donation_information_for_output)
def test_output_donation_data():
    """Test which functions are called if there is donation data to output."""
    my_participant = Participant(fake_participant_conf)
    my_participant._donation_list = ["a donor", "another_donor"]
    my_participant._top_donation = donation_for_output
    my_participant.output_donation_data()
    fake_participant._format_donation_information_for_output.assert_called()
    fake_participant.write_text_files.assert_called()


@mock.patch.object(eldonationtracker.api.participant.Participant, 'write_text_files', fake_participant.write_text_files)
@mock.patch.object(eldonationtracker.api.participant.Participant, '_format_donation_information_for_output',
                   fake_participant._format_donation_information_for_output)
def test_output_donation_data_no_top_donation():
    """Test which functions are called if there is donation data to ouput."""
    my_participant = Participant(fake_participant_conf)
    my_participant._donation_list = ["a donor", "another_donor"]
    my_participant.output_donation_data()
    fake_participant._format_donation_information_for_output.assert_called()
    fake_participant.write_text_files.assert_called()


@mock.patch.object(eldonationtracker.api.participant.Participant, 'write_text_files', fake_participant.write_text_files)
@mock.patch.object(eldonationtracker.api.participant.Participant, '_format_donor_information_for_output',
                   fake_participant._format_donor_information_for_output)
def test_output_donor_data_no_donations():
    my_participant = Participant(fake_participant_conf)
    my_participant.output_donor_data()
    fake_participant._format_donor_information_for_output.assert_not_called()
    fake_participant.write_text_files.assert_called()


@mock.patch.object(eldonationtracker.api.participant.Participant, 'write_text_files', fake_participant.write_text_files)
@mock.patch.object(eldonationtracker.api.participant.Participant, '_format_donor_information_for_output',
                   fake_participant._format_donor_information_for_output)
def test_output_donor_data():
    my_participant = Participant(fake_participant_conf)
    my_participant._donation_list = ["a donor", "another_donor"]
    my_participant._top_donor = "a top donor"
    my_participant.output_donor_data()
    assert fake_participant._format_donor_information_for_output.called
    assert fake_participant.write_text_files.called


@mock.patch.object(eldonationtracker.api.participant.Participant, 'write_text_files', fake_participant.write_text_files)
@mock.patch.object(eldonationtracker.api.participant.Participant, '_format_donor_information_for_output',
                   fake_participant._format_donor_information_for_output)
def test_output_donor_data_no_top_donor():
    my_participant = Participant(fake_participant_conf)
    my_participant._donation_list = ["a donor", "another_donor"]
    my_participant.output_donor_data()
    assert fake_participant._format_donor_information_for_output.called
    assert fake_participant.write_text_files.called


fake_extralife_io.read_in_total_raised.return_value = ''


@mock.patch.object(eldonationtracker.utils.extralife_io, 'read_in_total_raised', fake_extralife_io.read_in_total_raised)
def test_check_existence_of_text_files_no_value():
    my_participant = Participant(fake_participant_conf)
    is_there_a_text_file = my_participant._check_existence_of_text_files()
    assert is_there_a_text_file is False


fake_extralife_io.read_in_total_raised_low.return_value = '500.00'


@mock.patch.object(eldonationtracker.utils.extralife_io, 'read_in_total_raised',
                   fake_extralife_io.read_in_total_raised_low)
def test_check_existence_of_text_files_low_value():
    my_participant = Participant(fake_participant_conf)
    is_there_a_text_file = my_participant._check_existence_of_text_files()
    assert is_there_a_text_file is True


fake_extralife_io.read_in_total_raised_high.return_value = '1,500.00'


@mock.patch.object(eldonationtracker.utils.extralife_io, 'read_in_total_raised',
                   fake_extralife_io.read_in_total_raised_high)
def test_check_existence_of_text_files_high_value():
    my_participant = Participant(fake_participant_conf)
    is_there_a_text_file = my_participant._check_existence_of_text_files()
    assert is_there_a_text_file is True



fake_output_badge_data = mock.Mock()
fake_output_milestone_data = mock.Mock()


@mock.patch.object(eldonationtracker.api.participant.Participant, 'update_participant_attributes',
                   fake_participant_for_run.update_participant_attributes)
@mock.patch.object(eldonationtracker.api.participant.Participant, 'output_participant_data',
                   fake_participant_for_run.output_participant_data)
@mock.patch.object(eldonationtracker.api.participant.Participant, 'update_donation_data',
                   fake_participant_for_run.update_donation_data)
@mock.patch.object(eldonationtracker.api.participant.Participant, 'output_donation_data',
                   fake_participant_for_run.output_donation_data)
@mock.patch.object(eldonationtracker.api.participant.Participant, 'update_donor_data',
                   fake_participant_for_run.update_donor_data)
@mock.patch.object(eldonationtracker.api.participant.Participant, 'output_donor_data',
                   fake_participant_for_run.output_donor_data)
@mock.patch.object(eldonationtracker.api.team.Team, 'team_run', fake_participant_for_run.my_team.team_run)
@mock.patch.object(eldonationtracker.api.team.Team, 'participant_run',
                   fake_participant_for_run.my_team.participant_run)
@mock.patch.object(eldonationtracker.utils.extralife_io, "get_badges", magic_fake_badges.get_badges)
@mock.patch.object(eldonationtracker.utils.extralife_io, "output_badge_data", fake_output_badge_data)
@mock.patch.object(eldonationtracker.api.participant.Participant, '_update_milestones',
                   fake_participant_for_run._update_milestones)
@mock.patch.object(eldonationtracker.api.participant.Participant, 'output_milestone_data',
                   fake_participant_for_run.output_milestone_data)
@mock.patch.object(eldonationtracker.api.participant.Participant, '_update_incentives',
                   fake_participant_for_run.fake_participant_for_run._update_incentives)
@mock.patch.object(eldonationtracker.api.participant.Participant, 'output_incentive_data',
                   fake_participant_for_run.output_incentive_data)
def test_run():
    my_participant = Participant(fake_participant_conf)
    assert my_participant.number_of_donations == 0
    assert my_participant._first_run
    my_participant._goal = 500  # needed to make below run - will probably be fixed with better tests in future
    my_participant.run()
    fake_participant_for_run.update_participant_attributes.assert_called_once()
    fake_participant_for_run.output_participant_data.assert_called_once()
    fake_participant_for_run.update_donation_data.assert_called_once()
    fake_participant_for_run.output_donation_data.assert_called_once()
    fake_participant_for_run.update_donor_data.assert_called_once()
    fake_participant_for_run.my_team.team_run.assert_called_once()
    assert my_participant._first_run is False
    my_participant.run()
    assert fake_participant_for_run.update_participant_attributes.call_count == 2
    assert fake_participant_for_run.output_participant_data.call_count == 2
    fake_participant_for_run.update_donation_data.assert_called_once()
    fake_participant_for_run.output_donation_data.assert_called_once()
    fake_participant_for_run.update_donor_data.assert_called_once()
    assert fake_participant_for_run.my_team.team_run.call_count == 2


@mock.patch.object(eldonationtracker.utils.extralife_io, "get_json", fake_extralife_io.get_json)
@mock.patch.object(eldonationtracker.api.participant.Participant, 'output_participant_data',
                   fake_participant_for_run.output_participant_data)
@mock.patch.object(eldonationtracker.api.participant.Participant, 'update_donation_data',
                   fake_participant_for_run.update_donation_data)
@mock.patch.object(eldonationtracker.api.participant.Participant, 'output_donation_data',
                   fake_participant_for_run.output_donation_data)
@mock.patch.object(eldonationtracker.api.participant.Participant, 'update_donor_data',
                   fake_participant_for_run.update_donor_data)
@mock.patch.object(eldonationtracker.api.participant.Participant, 'output_donor_data',
                   fake_participant_for_run.output_donor_data)
@mock.patch.object(eldonationtracker.api.team.Team, 'team_run', fake_participant_for_run.my_team.team_run)
@mock.patch.object(eldonationtracker.api.team.Team, 'participant_run',
                   fake_participant_for_run.my_team.participant_run)
@mock.patch.object(eldonationtracker.utils.extralife_io, "get_badges", magic_fake_badges.get_badges)
@mock.patch.object(eldonationtracker.utils.extralife_io, "output_badge_data", fake_output_badge_data)
@mock.patch.object(eldonationtracker.api.participant.Participant, '_update_milestones',
                   fake_participant_for_run._update_milestones)
@mock.patch.object(eldonationtracker.api.participant.Participant, 'output_milestone_data',
                   fake_participant_for_run.output_milestone_data)
@mock.patch.object(eldonationtracker.api.participant.Participant, '_update_incentives',
                   fake_participant_for_run.fake_participant_for_run._update_incentives)
@mock.patch.object(eldonationtracker.api.participant.Participant, 'output_incentive_data',
                   fake_participant_for_run.output_incentive_data)
def test_run_get_a_donation():
    fake_participant_for_run.output_participant_data.reset_mock()
    fake_participant_for_run.update_donation_data.reset_mock()
    fake_participant_for_run.output_donation_data.reset_mock()
    fake_participant_for_run.update_donor_data.reset_mock()
    fake_participant_for_run.output_donor_data.reset_mock()
    fake_participant_for_run.my_team.team_run.reset_mock()
    fake_participant_for_run.my_team.participant_run.reset_mock()
    my_participant = Participant(fake_participant_conf)
    assert my_participant.number_of_donations == 0
    my_participant._first_run = False  # to simulate that this is after one run already
    my_participant._donor_list = ['this is fake mocked and does not matter']
    my_participant.run()
    fake_participant_for_run.output_participant_data.assert_called_once()
    fake_participant_for_run.update_donation_data.assert_called_once()
    fake_participant_for_run.output_donation_data.assert_called_once()
    fake_participant_for_run.update_donor_data.assert_called_once()
    fake_participant_for_run.output_donor_data.assert_called_once()
    fake_participant_for_run.my_team.team_run.assert_called_once()


@mock.patch.object(eldonationtracker.api.participant.Participant, 'write_text_files', fake_participant.write_text_files)
@mock.patch.object(eldonationtracker.api.team.Team, 'team_run', fake_participant_for_run.my_team.team_run)
@mock.patch.object(eldonationtracker.api.team.Team, 'participant_run',
                   fake_participant_for_run.my_team.participant_run)
@mock.patch.object(eldonationtracker.utils.extralife_io, "get_badges", magic_fake_badges.get_badges)
@mock.patch.object(eldonationtracker.utils.extralife_io, "output_badge_data", fake_output_badge_data)
@mock.patch.object(eldonationtracker.api.participant.Participant, '_update_milestones',
                   fake_participant_for_run._update_milestones)
@mock.patch.object(eldonationtracker.api.participant.Participant, 'output_milestone_data',
                   fake_participant_for_run.output_milestone_data)
@mock.patch.object(eldonationtracker.api.participant.Participant, '_update_incentives',
                   fake_participant_for_run.fake_participant_for_run._update_incentives)
@mock.patch.object(eldonationtracker.api.participant.Participant, 'output_incentive_data',
                   fake_participant_for_run.output_incentive_data)
def test_run_no_api_hit():
    """Making sure that output data is not hit if API wasn't hit."""
    fake_participant_for_run.output_participant_data.reset_mock()
    my_participant = Participant(fake_participant_conf)
    my_participant.run()
    fake_participant_for_run.output_participant_data.assert_not_called()


@mock.patch.object(eldonationtracker.api.participant.Participant, 'write_text_files', fake_participant.write_text_files)
@mock.patch.object(eldonationtracker.api.team.Team, 'team_run', fake_participant_for_run.my_team.team_run)
@mock.patch.object(eldonationtracker.api.team.Team, 'participant_run',
                   fake_participant_for_run.my_team.participant_run)
@mock.patch.object(eldonationtracker.utils.extralife_io, "get_badges", magic_fake_badges.get_badges)
@mock.patch.object(eldonationtracker.utils.extralife_io, "output_badge_data", fake_output_badge_data)
@mock.patch.object(eldonationtracker.api.participant.Participant, '_update_milestones',
                   fake_participant_for_run._update_milestones)
@mock.patch.object(eldonationtracker.api.participant.Participant, 'output_milestone_data',
                   fake_participant_for_run.output_milestone_data)
@mock.patch.object(eldonationtracker.api.participant.Participant, '_update_incentives',
                   fake_participant_for_run.fake_participant_for_run._update_incentives)
@mock.patch.object(eldonationtracker.api.participant.Participant, 'output_incentive_data',
                   fake_participant_for_run.output_incentive_data)
def test_run_no_api_hit_no_team():
    """Making sure that output data is not hit if API wasn't hit."""
    fake_participant_for_run.output_participant_data.reset_mock()
    fake_participant_for_run.my_team.team_run.reset_mock()
    fake_participant_for_run.my_team.participant_run.reset_mock()
    my_participant = Participant(fake_participant_conf_no_team)
    my_participant.run()
    fake_participant_for_run.output_participant_data.assert_not_called()
    fake_participant_for_run.my_team.team_run.assert_not_called()
