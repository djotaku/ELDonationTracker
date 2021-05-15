# type: ignore

from dataclasses import dataclass


@dataclass
class Badge:
    """Achievement Badges associated with a Participant or Team.

    For Donor Drive API information: https://github.com/DonorDrive/PublicAPI/blob/master/resources/badges.md

    :param badge_code: A unique identifier for this badge.
    :type: str
    :param badge_image_url: The URL for the image associated with this badge
    :type: str
    :param description: The description of this badge
    :type: str
    :param title: The title of this badge
    :type: str
    :param unlocked_date_utc: The date this badge was unlocked by the Participant or Team
    :type: str
    """
    badge_code: str
    badge_image_url: str
    description: str
    title: str
    unlocked_date_utc: str

    @staticmethod
    def create_badge(json_data: dict):
        """Create a badge based on the JSON data.

        :param json_data: The JSON data for this badge.
        :type: dict
        :returns: a Badge object
        """
        return Badge(json_data.get("badgeCode"), json_data.get("badgeImageURL"), json_data.get("description"),
                     json_data.get('title'), json_data.get("unlockedDateUTC"))
