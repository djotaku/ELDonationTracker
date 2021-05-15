from eldonationtracker.api import badge
import json


def test_badge_creation():
    """Test creation of a badge ojbect."""
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
    test_badges = [badge.Badge.create_badge(a_badge) for a_badge in example_json_as_json]
    assert test_badges[0].badge_code == "100-club-badge"
    assert test_badges[0].badge_image_url == "http://assets.donordrive.com/try/images/$event508$/badge_2F7819D3_C019_3C7D_B9D716687CEEC0A5.png"
    assert test_badges[0].description == "Raised 100 dollars!"
    assert test_badges[0].title == "100 Club Badge"
    assert test_badges[0].unlocked_date_utc == "2019-10-30T18:01:23.430+0000"
    assert test_badges[1].badge_code == "enthusiastic-participant-badge"
    assert test_badges[1].badge_image_url == "https://assets.donordrive.com/try/images/$event508$/badge_DCB0A883_BC0A_97DB_639B4D7BFDEC638E.png"
    assert test_badges[1].description == "Sent 25 donation invite emails!"
    assert test_badges[1].title == "Enthusiastic Participant Badge"
    assert test_badges[1].unlocked_date_utc == "2019-09-18T15:47:39.107+0000"
