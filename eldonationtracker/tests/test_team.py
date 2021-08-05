"""Unit tests for team.py."""

from unittest import mock

from eldonationtracker.api import team as team


def test_team_urls():
    """Test that URL construction is correct."""
    my_team = team.Team("12345", "folder", "$", "5")
    assert my_team.team_url == "https://www.extra-life.org/api/teams/12345"
    assert my_team.team_participant_url == "https://www.extra-life.org/api/teams/12345/participants"
    assert my_team.team_donation_url == "https://www.extra-life.org/api/teams/12345/donations"


def test_output_folder():
    """Test that the program correctly parses the output folder."""
    my_team = team.Team("12345", "folder", "$", "5")
    assert my_team.output_folder == "folder"


def test_donors_to_display():
    """Test that the program correct parses the number of donors to display."""
    my_team = team.Team("12345", "folder", "$", "5")
    assert my_team.donors_to_display == "5"


def test_get_team_json():
    """Test that the JSON we get back is correctly interpreted."""
    with mock.patch("eldonationtracker.api.team.extralife_io.get_json",
                    return_value={"fundraisingGoal": 500, "captainDisplayName": "Captain Awesome",
                                  "sumDonations": 400, "numDonations": 300,
                                  "avatarImageURL": "//assets.donordrive.com/…avatar-team-default.gif"}):
        my_team = team.Team("12345", "folder", "$", "5")
        team_json = my_team._get_team_json()
        assert team_json == (500, 'Captain Awesome', 400, 300, "//assets.donordrive.com/…avatar-team-default.gif")


def test_get_team_json_no_json():
    """Test to make sure if no JSON is returned from the endpoint, the program responds correcty."""
    with mock.patch("eldonationtracker.api.team.extralife_io.get_json", return_value={}):
        my_team = team.Team("12345", "folder", "$", "5")
        team_json = my_team._get_team_json()
        assert team_json == (0, '', 0, 0, '')
        # let's pretend that at some point values were added
        # but now the API can't be reached. Let's make sure it doesn't over-write the good data.
        my_team._team_goal = 500
        my_team._team_captain = 'Captain Awesome'
        my_team._total_raised = 400
        my_team._num_donations = 300
        my_team._team_avatar_image = "//assets.donordrive.com/…avatar-team-default.gif"
        team_json = my_team._get_team_json()
        assert team_json == (500, 'Captain Awesome', 400, 300, "//assets.donordrive.com/…avatar-team-default.gif")


def test_update_team_dictionary():
    my_team = team.Team("12345", "folder", "$", "5")
    my_team._team_goal = 500
    my_team._team_captain = 'Captain Awesome'
    my_team._total_raised = 400
    my_team._num_donations = 300
    my_team._update_team_dictionary()
    assert list(my_team._team_info.values()) == ['$500.00', 'Captain Awesome', '$400.00', '300']


def test_get_participants_no_participants():
    my_team = team.Team("12345", "folder", "$", "5")
    with mock.patch("eldonationtracker.api.team.extralife_io.get_json", return_value={}):
        participants = my_team._get_participants(False)
        assert participants == []
        assert my_team._participant_list == []


def test_get_participants():
    my_team = team.Team("12345", "folder", "$", "5")
    team_participants = [{"displayName":"Karl Abraham",
                          "fundraisingGoal":500.00,
                          "eventName":"Extra Life 2020",
                          "links":{"donate":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=411130#donate",
                                   "stream":"https://player.twitch.tv/?channel=ToxicAntidote",
                                   "page":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=411130"},
                          "createdDateUTC":"2020-05-31T23:08:31.103+0000","eventID":547,"sumDonations":0.00,
                          "participantID":411130,"teamName":"Giant Bomb",
                          "avatarImageURL":"//assets.donordrive.com/extralife/images/$avatars$/constituent_18EE04BD-BBCC-439D-B1DC6C5B9FCD9130.jpg",
                          "streamIsLive":False,"teamID":50394,"isTeamCaptain":False,"sumPledges":0.00,"numDonations":0},
                         {"displayName":"Ben Tolmachoff","fundraisingGoal":500.00,"eventName":"Extra Life 2020",
                          "links":{"donate":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=411107#donate",
                                   "stream":"https://player.twitch.tv/?channel=chof",
                                   "page":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=411107"},
                          "createdDateUTC":"2020-05-30T21:34:38.133+0000","eventID":547,"sumDonations":0.00,
                          "participantID":411107,"teamName":"Giant Bomb",
                          "avatarImageURL":"//assets.donordrive.com/extralife/images/$avatars$/constituent_FACE6F26-A2A6-80BB-F35771F8733FBEBE.jpg",
                          "streamIsLive":False,"teamID":50394,"isTeamCaptain":False,"sumPledges":0.00,"numDonations":0},
                         {"displayName":"Michael Bataligin","fundraisingGoal":100.00,"eventName":"Extra Life 2020",
                          "links":{"donate":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=410654#donate",
                                   "page":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=410654"},
                          "createdDateUTC":"2020-05-23T00:19:14.707+0000","eventID":547,"sumDonations":5.00,
                          "participantID":410654,"teamName":"Giant Bomb",
                          "avatarImageURL":"//assets.donordrive.com/extralife/images/$avatars$/constituent_0AFEA929-C29F-F29A-6B659B3718802B75.jpg",
                          "teamID":50394,"isTeamCaptain":False,"sumPledges":0.00,"numDonations":1}]
    with mock.patch("eldonationtracker.api.team.extralife_io.get_json", return_value=team_participants):
        participants = my_team._get_participants(False)
        assert participants[0].name == "Karl Abraham"
        assert participants[1].name == "Ben Tolmachoff"


def test_get_participants_no_participants_top_5():
    my_team = team.Team("12345", "folder", "$", "5")
    with mock.patch("eldonationtracker.api.team.extralife_io.get_json", return_value={}):
        participants = my_team._get_participants(True)
        assert participants == []
        assert my_team._top_5_participant_list == []


def test_get_participants_top_5():
    """Test getting top 5 participants.

    While, of course, in reality the JSON would be different - sorted by donations, in terms
    of what the code has to do with what it gets back, there is no difference. So I have just copied things
    to ensure I'm considering both parts of the if statement in this function.
    """
    my_team = team.Team("12345", "folder", "$", "5")
    team_participants = [{"displayName":"Karl Abraham",
                          "fundraisingGoal":500.00,
                          "eventName":"Extra Life 2020",
                          "links":{"donate":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=411130#donate",
                                   "stream":"https://player.twitch.tv/?channel=ToxicAntidote",
                                   "page":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=411130"},
                          "createdDateUTC":"2020-05-31T23:08:31.103+0000","eventID":547,"sumDonations":0.00,
                          "participantID":411130,"teamName":"Giant Bomb",
                          "avatarImageURL":"//assets.donordrive.com/extralife/images/$avatars$/constituent_18EE04BD-BBCC-439D-B1DC6C5B9FCD9130.jpg",
                          "streamIsLive":False,"teamID":50394,"isTeamCaptain":False,"sumPledges":0.00,"numDonations":0},
                         {"displayName":"Ben Tolmachoff","fundraisingGoal":500.00,"eventName":"Extra Life 2020",
                          "links":{"donate":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=411107#donate",
                                   "stream":"https://player.twitch.tv/?channel=chof",
                                   "page":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=411107"},
                          "createdDateUTC":"2020-05-30T21:34:38.133+0000","eventID":547,"sumDonations":0.00,
                          "participantID":411107,"teamName":"Giant Bomb",
                          "avatarImageURL":"//assets.donordrive.com/extralife/images/$avatars$/constituent_FACE6F26-A2A6-80BB-F35771F8733FBEBE.jpg",
                          "streamIsLive":False,"teamID":50394,"isTeamCaptain":False,"sumPledges":0.00,"numDonations":0},
                         {"displayName":"Michael Bataligin","fundraisingGoal":100.00,"eventName":"Extra Life 2020",
                          "links":{"donate":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=410654#donate",
                                   "page":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=410654"},
                          "createdDateUTC":"2020-05-23T00:19:14.707+0000","eventID":547,"sumDonations":5.00,
                          "participantID":410654,"teamName":"Giant Bomb",
                          "avatarImageURL":"//assets.donordrive.com/extralife/images/$avatars$/constituent_0AFEA929-C29F-F29A-6B659B3718802B75.jpg",
                          "teamID":50394,"isTeamCaptain":False,"sumPledges":0.00,"numDonations":1}]
    with mock.patch("eldonationtracker.api.team.extralife_io.get_json", return_value=team_participants):
        participants = my_team._get_participants(True)
        assert participants[0].name == "Karl Abraham"
        assert participants[1].name == "Ben Tolmachoff"


def test_top_participant_no_participants():
    my_team = team.Team("12345", "folder", "$", "5")
    top_participant = my_team._top_participant()
    assert top_participant == "No participants."


def test_top_participant():
    my_team = team.Team("12345", "folder", "$", "5")
    team_participants = [{"displayName":"Karl Abraham",
                          "fundraisingGoal":500.00,
                          "eventName":"Extra Life 2020",
                          "links":{"donate":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=411130#donate",
                                   "stream":"https://player.twitch.tv/?channel=ToxicAntidote",
                                   "page":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=411130"},
                          "createdDateUTC":"2020-05-31T23:08:31.103+0000","eventID":547,"sumDonations":0.00,
                          "participantID":411130,"teamName":"Giant Bomb",
                          "avatarImageURL":"//assets.donordrive.com/extralife/images/$avatars$/constituent_18EE04BD-BBCC-439D-B1DC6C5B9FCD9130.jpg",
                          "streamIsLive":False,"teamID":50394,"isTeamCaptain":False,"sumPledges":0.00,"numDonations":0},
                         {"displayName":"Ben Tolmachoff","fundraisingGoal":500.00,"eventName":"Extra Life 2020",
                          "links":{"donate":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=411107#donate",
                                   "stream":"https://player.twitch.tv/?channel=chof",
                                   "page":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=411107"},
                          "createdDateUTC":"2020-05-30T21:34:38.133+0000","eventID":547,"sumDonations":0.00,
                          "participantID":411107,"teamName":"Giant Bomb",
                          "avatarImageURL":"//assets.donordrive.com/extralife/images/$avatars$/constituent_FACE6F26-A2A6-80BB-F35771F8733FBEBE.jpg",
                          "streamIsLive":False,"teamID":50394,"isTeamCaptain":False,"sumPledges":0.00,"numDonations":0},
                         {"displayName":"Michael Bataligin","fundraisingGoal":100.00,"eventName":"Extra Life 2020",
                          "links":{"donate":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=410654#donate",
                                   "page":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=410654"},
                          "createdDateUTC":"2020-05-23T00:19:14.707+0000","eventID":547,"sumDonations":5.00,
                          "participantID":410654,"teamName":"Giant Bomb",
                          "avatarImageURL":"//assets.donordrive.com/extralife/images/$avatars$/constituent_0AFEA929-C29F-F29A-6B659B3718802B75.jpg",
                          "teamID":50394,"isTeamCaptain":False,"sumPledges":0.00,"numDonations":1}]
    with mock.patch("eldonationtracker.api.team.extralife_io.get_json", return_value=team_participants):
        my_team._top_5_participant_list = my_team._get_participants(True)
        top_participant = my_team._top_participant()
        assert top_participant == "Karl Abraham - $0.00"


def test_participant_calculations_no_data():
    """What if the API comes back empty? Maybe a team just formed without any members?"""
    my_team = team.Team("12345", "folder", "$", "5")
    my_team._participant_calculations()
    assert my_team._participant_calculation_dict['Team_TopParticipantNameAmnt'] == "No participants."
    assert my_team._participant_calculation_dict['Team_Top5ParticipantsHorizontal'] == ""
    assert my_team._participant_calculation_dict['Team_Top5Participants'] == ""


def test_participant_calculations():
    my_team = team.Team("12345", "folder", "$", "5")
    team_participants = [{"displayName":"Karl Abraham",
                          "fundraisingGoal":500.00,
                          "eventName":"Extra Life 2020",
                          "links":{"donate":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=411130#donate",
                                   "stream":"https://player.twitch.tv/?channel=ToxicAntidote",
                                   "page":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=411130"},
                          "createdDateUTC":"2020-05-31T23:08:31.103+0000","eventID":547,"sumDonations":0.00,
                          "participantID":411130,"teamName":"Giant Bomb",
                          "avatarImageURL":"//assets.donordrive.com/extralife/images/$avatars$/constituent_18EE04BD-BBCC-439D-B1DC6C5B9FCD9130.jpg",
                          "streamIsLive":False,"teamID":50394,"isTeamCaptain":False,"sumPledges":0.00,"numDonations":0},
                         {"displayName":"Ben Tolmachoff","fundraisingGoal":500.00,"eventName":"Extra Life 2020",
                          "links":{"donate":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=411107#donate",
                                   "stream":"https://player.twitch.tv/?channel=chof",
                                   "page":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=411107"},
                          "createdDateUTC":"2020-05-30T21:34:38.133+0000","eventID":547,"sumDonations":0.00,
                          "participantID":411107,"teamName":"Giant Bomb",
                          "avatarImageURL":"//assets.donordrive.com/extralife/images/$avatars$/constituent_FACE6F26-A2A6-80BB-F35771F8733FBEBE.jpg",
                          "streamIsLive":False,"teamID":50394,"isTeamCaptain":False,"sumPledges":0.00,"numDonations":0},
                         {"displayName":"Michael Bataligin","fundraisingGoal":100.00,"eventName":"Extra Life 2020",
                          "links":{"donate":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=410654#donate",
                                   "page":"https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=410654"},
                          "createdDateUTC":"2020-05-23T00:19:14.707+0000","eventID":547,"sumDonations":5.00,
                          "participantID":410654,"teamName":"Giant Bomb",
                          "avatarImageURL":"//assets.donordrive.com/extralife/images/$avatars$/constituent_0AFEA929-C29F-F29A-6B659B3718802B75.jpg",
                          "teamID":50394,"isTeamCaptain":False,"sumPledges":0.00,"numDonations":1}]
    with mock.patch("eldonationtracker.api.team.extralife_io.get_json", return_value=team_participants):
        my_team._top_5_participant_list = my_team._get_participants(True)
        my_team._participant_calculations()
        assert my_team._participant_calculation_dict['Team_TopParticipantNameAmnt'] == "Karl Abraham - $0.00"
        assert my_team._participant_calculation_dict['Team_Top5ParticipantsHorizontal'] == "Karl Abraham - $0.00 | Ben Tolmachoff - $0.00 | Michael Bataligin - $5.00 | "
        assert my_team._participant_calculation_dict['Team_Top5Participants'] == "Karl Abraham - $0.00\nBen Tolmachoff - $0.00\nMichael Bataligin - $5.00\n"


fake_get_team_json = mock.Mock()
fake_get_team_json.return_value = 400, "Captain", 401, 3, "//assets.donordrive.com/…avatar-team-default.gif"
fake_participant_run = mock.Mock()
fake_write_text_files = mock.Mock()
fake_donation_run = mock.Mock()
fake_badge_run = mock.Mock()


@mock.patch.object(team.Team, "_get_team_json", fake_get_team_json)
@mock.patch.object(team.Team, "participant_run", fake_participant_run)
@mock.patch.object(team.Team, "write_text_files", fake_write_text_files)
@mock.patch.object(team.Team, "donation_run", fake_donation_run)
def test_team_run():
    my_team = team.Team("12345", "folder", "$", "5")
    my_team.team_run()
    assert fake_participant_run.call_count == 1
    my_team.team_run()
    assert fake_participant_run.call_count == 1
    fake_get_team_json.return_value = 400, "Captain", 402, 4, "//assets.donordrive.com/…avatar-team-default.gif"
    my_team.team_run()
    assert fake_participant_run.call_count == 2


fake_get_team_json2 = mock.Mock()
fake_get_team_json2.return_value = 400, "Captain", 401, 3, "//assets.donordrive.com/…avatar-team-default.gif"
fake_output_badge_data = mock.Mock()


@mock.patch.object(team.Team, "_get_team_json", fake_get_team_json2)
@mock.patch.object(team.Team, "participant_run", fake_participant_run)
@mock.patch.object(team.Team, "write_text_files", fake_write_text_files)
@mock.patch.object(team.Team, "donation_run", fake_donation_run)
@mock.patch.object(team.Team, "_update_badges", fake_badge_run)
@mock.patch.object(team.extralife_io, "output_badge_data", fake_output_badge_data)
def test_team_api_info():
    my_team = team.Team("12345", "folder", "$", "5")
    my_team.team_api_info()
    assert my_team.team_goal == 400
    assert my_team.team_captain == "Captain"
    assert my_team.total_raised == 401
    assert my_team.num_donations == 3
    assert my_team._team_info["Team_goal"] == '$400.00'
    assert my_team._team_info["Team_captain"] == "Captain"
    assert my_team._team_info["Team_totalRaised"] == "$401.00"
    assert my_team._team_info["Team_numDonations"] == '3'


def test_str_no_json_data():
    """Test what str will produce if the JSON retrieval hasn't yet run."""
    my_team = team.Team("12345", "folder", "$", "5")
    assert str(my_team) == "A team found at https://www.extra-life.org/api/teams/12345. "


def test_str():
    """Test what str will produce after team_info has been filled out."""
    my_team = team.Team("12345", "folder", "$", "5")
    my_team._team_info["Team_goal"] = '$400.00'
    assert str(my_team) == "A team found at https://www.extra-life.org/api/teams/12345. Team goal is $400.00."


def test_str_no_json_data_no_team_id():
    """Test what str will produce if the JSON retrieval hasn't yet run AND no team ID.

    This would happen if the user is not part of a team.
    """
    my_team = team.Team(None, "folder", "$", "5")
    assert str(my_team) == "Not a valid team - no team_id."
