"""Grabs Participant JSON data and outputs to files."""

from dataclasses import dataclass, field
import logging
from rich import print  # type ignore
from rich.logging import RichHandler  # type ignore
import time

import eldonationtracker.utils.extralife_io
from eldonationtracker.api import donor as donor, team as team, donation as donation, badge
from eldonationtracker.utils import extralife_io as extralife_io
from eldonationtracker import base_api_url

# logging
participant_log = logging.getLogger("Participant")
participant_log.setLevel(logging.INFO)


class Participant:
    """Owns all the attributes under the participant API.

    Also owns the results of any calculated data.

    Donor Drive API api info at https://github.com/DonorDrive/PublicAPI
    """

    def __init__(self, config):
        """Load in config from participant.conf and initialize participant variables.
        """
        self.config = config
        self._extralife_id: str = ""
        self._text_folder: str = ""
        self._currency_symbol: str = ""
        self._team_id: str = ""
        self._donors_to_display: str = ""
        self._participant_url: str = ""
        self._donation_url: str = ""
        self._participant_donor_url: str = ""
        self._my_team: team.Team = None

        # Participant Information
        self._total_raised: int = 0
        self._number_of_donations: int = 0
        self._average_donation: int = 0
        self._goal: int = 0
        self._avatar_image_url: str = ""
        self._event_name: str = ""
        self._donation_link_url: str = ""
        self._stream_url: str = ""
        self._extra_life_page_url: str = ""
        self._created_date_utc: str = ""
        self._stream_is_live: bool = False
        self._sum_pledges: int = 0
        self._team_name: str = ""
        self._is_team_captain: bool = False
        self._display_name: str = ''

        self._participant_formatted_output = {'totalRaised': f"{self.currency_symbol}0.00",
                                              'averageDonation': f"{self.currency_symbol}0.00",
                                              'goal': f"{self.currency_symbol}0.00"}

        # donation information
        self._donation_list: list[donation] = []
        self._ordered_donation_list: list[donation] = []
        self._top_donation = None
        self._top_donation_formatted_output: dict = {'TopDonationNameAmnt': "No Donations Yet"}
        self._donation_formatted_output: dict = {'LastDonationNameAmnt': "No Donations Yet",
                                                 'lastNDonationNameAmts': "No Donations Yet",
                                                 'lastNDonationNameAmtsMessage': "No Donations Yet",
                                                 'lastNDonationNameAmtsMessageHorizontal': "No Donations Yet",
                                                 'lastNDonationNameAmtsHorizontal': "No Donations Yet"}
        # donor information
        self._top_donor = None
        self._top_donor_formatted_output: dict = {'TopDonorNameAmnt': "No Donors Yet"}
        self._donor_list: list[donor] = []
        self._ordered_donor_list: list[donor] = []
        self._donor_formatted_output: dict = {'LastDonorNameAmnt': "No Donations Yet",
                                              'lastNDonorNameAmts': "No Donations Yet",
                                              'lastNDonorNameAmtsMessage': "No Donations Yet",
                                              'lastNDonorNameAmtsMessageHorizontal': "No Donations Yet",
                                              'lastNDonorNameAmtsHorizontal': "No Donations Yet"}

        # other API endpoints
        self._badge_url: str = ''
        self._badges: list[badge.Badge] = []
        self._milestone_url: str = ''
        self._milestones: list[Milestone] = []
        self._incentive_url: str = ''
        self._incentives: list[Incentive] = []

        # misc
        self._first_run: bool = True
        self._new_donation: bool = False
        self._text_files_exist: bool = False

        self.set_config_values()

    @property
    def extralife_id(self) -> str:
        """The participant's extra life ID"""
        return self._extralife_id

    @property
    def text_folder(self) -> str:
        """Where the output text files will be written on disk"""
        return self._text_folder

    @property
    def currency_symbol(self) -> str:
        """The currency symbol eg '$' added to the output text files."""
        return self._currency_symbol

    @property
    def team_id(self) -> str:
        """The Team ID if the participant is part of a team."""
        return self._team_id

    @property
    def donors_to_display(self) -> str:
        """For output text files that display multiple donors (or donations), the number of them that
        should be written to the text file.
        """
        return self._donors_to_display

    @property
    def participant_url(self) -> str:
        """API endpoint for the participant"""
        return self._participant_url

    @property
    def donation_url(self) -> str:
        """API endpoint for the Participant's donations."""
        return self._donation_url

    @property
    def participant_donor_url(self) -> str:
        """API Endpoint for the Participant's donors."""
        return self._participant_donor_url

    @property
    def my_team(self) -> team.Team:
        """An instantiation of a team class for the participant's team."""
        return self._my_team

    @property
    def total_raised(self) -> int:
        """Total amount raised by the participant."""
        return self._total_raised

    @property
    def number_of_donations(self) -> int:
        """The number of donations received by the participant."""
        return self._number_of_donations

    @property
    def average_donation(self) -> int:
        """The average amount of donations received by this participant"""
        return self._average_donation

    @property
    def goal(self) -> int:
        """The goal for the amount of the money the participant wishes to raise."""
        return self._goal

    @property
    def avatar_image_url(self) -> str:
        """The user's avatar image on the website."""
        if self._avatar_image_url:
            return self._avatar_image_url
        else:
            return ""

    @property
    def event_name(self) -> str:
        """The event name as obtained from the API."""
        return self._event_name

    @property
    def donation_link_url(self) -> str:
        """The link for making donations to the participant."""
        return self._donation_link_url

    @property
    def stream_url(self) -> str:
        """The URL to the participant's stream on Twitch."""
        return self._stream_url

    @property
    def stream_is_live(self) -> bool:
        """True if the participant is actively streaming."""
        return self._stream_is_live

    @property
    def extra_life_page_url(self) -> str:
        """The URL to the participant's ExtraLife page."""
        return self._extra_life_page_url

    @property
    def created_date_utc(self) -> str:
        """The date the participant created their campaign."""
        return self._created_date_utc

    @property
    def team_name(self) -> str:
        """If the participant is part of a team, this is the team name."""
        return self._team_name

    @property
    def is_team_captain(self) -> bool:
        """True if the participant is the team captain."""
        return self._is_team_captain

    @property
    def sum_pledges(self) -> int:
        """Number of pledges for the participant."""
        return self._sum_pledges

    @property
    def new_donation(self) -> bool:
        """True if the participant receives a new donation."""
        return self._new_donation

    @new_donation.setter
    def new_donation(self, new_donation_status: bool):
        """Change the _new_donation status."""
        self._new_donation = new_donation_status

    @property
    def display_name(self) -> str:
        """Return the participant's display name."""
        return self._display_name

    @property
    def badge_url(self) -> str:
        """Return the participant's badge URL"""
        return self._badge_url

    @property
    def badges(self) -> list[badge.Badge]:  # type: ignore
        """Return the list of participant badges."""
        return self._badges

    @property
    def milestone_url(self) -> str:
        """Return the Milestone URL"""
        return self._milestone_url

    @property
    def milestones(self):
        """Return a list of Milestones"""
        return self._milestones

    @property
    def incentive_url(self) -> str:
        """Return the Incentive URL"""
        return self._incentive_url

    @property
    def incentives(self):
        """Return a list of Incentives"""
        return self._incentives

    def set_config_values(self) -> None:
        """Set participant values, create URLs, and create Team."""
        (self._extralife_id, self._text_folder,
         self._currency_symbol, self._team_id,
         self._donors_to_display) = self.config.get_cli_values()
        # urls
        self._participant_url = f"{base_api_url}/participants/{self.extralife_id}"
        self._donation_url = f"{self.participant_url}/donations"
        self._participant_donor_url = f"{self.participant_url}/donors"
        self._badge_url = f"{self.participant_url}/badges"
        self._milestone_url = f"{self.participant_url}/milestones"
        self._incentive_url = f"{self.participant_url}/incentives"

        if self.team_id:
            self._my_team = team.Team(self.team_id, self.text_folder, self.currency_symbol, self.donors_to_display)

    def _get_participant_info(self):
        """Get JSON data for participant information.

        :returns: JSON data for self.total_raised, self.number_of_donations, and self.goal.
        """
        participant_json = extralife_io.get_json(self.participant_url)
        if not participant_json:
            participant_log.warning("[bold red]Couldn't access participant JSON.[/bold red]")
            return self.total_raised, self.number_of_donations, self.goal, self.avatar_image_url, self.event_name, \
                self.donation_link_url, self.stream_url, self.extra_life_page_url, self.created_date_utc,\
                self.stream_is_live, self.sum_pledges, self.team_name, self.is_team_captain, self.display_name
        else:
            if self.my_team:
                team_name = participant_json.get('teamName')
                is_team_captain = participant_json.get('isTeamCaptain')
            else:
                team_name = ''
                is_team_captain = False
            return participant_json.get('sumDonations'), participant_json.get('numDonations'), \
                participant_json.get('fundraisingGoal'), participant_json.get('avatarImageURL'), \
                participant_json.get('eventName'), participant_json.get('links').get("donate"), \
                participant_json.get('links').get('stream'), participant_json.get('links').get('page'), \
                participant_json.get('createdDateUTC'), participant_json.get("streamIsLive"), \
                participant_json.get('sumPledges'), team_name, is_team_captain, participant_json.get('displayName')

    def _format_participant_info_for_output(self, participant_attribute) -> str:
        """Format participant info for output to text files.

        :param participant_attribute: the data to be formatted for the output.
        :returns: A string with the formatted information.
        """
        return f"{self.currency_symbol}{participant_attribute:,.2f}"

    def _fill_participant_dictionary(self) -> None:
        """Fill up self.participant_formatted_output ."""
        self._participant_formatted_output["totalRaised"] = \
            self._format_participant_info_for_output(self.total_raised)
        self._participant_formatted_output["averageDonation"] = \
            self._format_participant_info_for_output(self.average_donation)
        self._participant_formatted_output["goal"] = self._format_participant_info_for_output(self.goal)
        self._participant_formatted_output["numDonations"] = str(self.number_of_donations)

    def _calculate_average_donation(self):
        """Calculate the average donation amount.

        :returns: The average or 0.
        """
        try:
            return self.total_raised / self.number_of_donations
        except ZeroDivisionError:
            return 0

    def _get_top_donations(self):  # pragma: no cover
        """Return top donations from server.

        Uses donor drive's sorting to get the top donation."""
        return extralife_io.get_donations(self._ordered_donation_list, self.donation_url, True, True)

    def _get_top_donors(self):  # pragma: no cover
        """Return Top Donors from server.

        Uses donor drive's sorting to get the top guy or gal.
        """
        return extralife_io.get_donations(self._ordered_donor_list, self.participant_donor_url, False, True)

    def _get_donors(self):  # pragma: no cover
        """Return Donors from server."""
        return extralife_io.get_donations(self._ordered_donor_list, self.participant_donor_url, False, False)

    def _format_donor_information_for_output(self) -> None:
        """Format the donor attributes for the output files."""
        self._top_donor_formatted_output['TopDonorNameAmnt'] = extralife_io.single_format(self._top_donor, False,
                                                                                          self.currency_symbol)
        self._donor_formatted_output = eldonationtracker.utils.extralife_io.format_information_for_output(
            self._donor_list, self.currency_symbol, self.donors_to_display, team=False, donation=False)

    def _format_donation_information_for_output(self) -> None:
        """Format the donation attributes for the output files."""
        self._donation_formatted_output = eldonationtracker.utils.extralife_io.format_information_for_output(
            self._donation_list, self.currency_symbol, self.donors_to_display, team=False)
        self._top_donation_formatted_output['TopDonationNameAmnt'] = extralife_io.single_format(self._top_donation,
                                                                                                False,
                                                                                                self.currency_symbol)

    def update_participant_attributes(self) -> None:  # pragma: no cover
        """Update participant attributes.

         A public method that will update the Participant object with data from self.participant_url.

         Also called from the main loop.
         """
        self._total_raised, self._number_of_donations, self._goal, self._avatar_image_url, \
            self._event_name, self._donation_link_url, self._stream_url, \
            self._extra_life_page_url, self._created_date_utc, self._stream_is_live, \
            self._sum_pledges, self._team_name, self._is_team_captain, self._display_name = self._get_participant_info()
        self._average_donation = self._calculate_average_donation()

    def output_participant_data(self) -> None:  # pragma: no cover
        """Format participant data and write to text files for use by OBS or XSplit.

        A public method to do the above. Also called from the main loop.
        """
        self._fill_participant_dictionary()
        self.write_text_files(self._participant_formatted_output)
        participant_avatar_for_html = "<img src=" + self.avatar_image_url + ">"
        extralife_io.write_html_files(participant_avatar_for_html, 'Participant_Avatar', self.text_folder)

    def update_donation_data(self) -> None:
        """Update donation data."""
        if self.number_of_donations > 0:
            self._donation_list = eldonationtracker.utils.extralife_io.get_donations(self._donation_list,
                                                                                     self.donation_url)
            self._ordered_donation_list = self._get_top_donations()
            try:
                self._top_donation = self._ordered_donation_list[0]
            except IndexError:  # pragma: no cover
                pass

    def update_donor_data(self) -> None:
        """Update donor data."""
        if self.number_of_donations > 0:
            self._donor_list = self._get_donors()
            # anonymous donors mess things up because they don't populate the donor API endpoint.
            # So this check prevents a crash.
            if self._donor_list:
                self._ordered_donor_list = self._get_top_donors()
                self._top_donor = self._ordered_donor_list[0]

    def _update_badges(self) -> None:
        """Add all our badges to the list."""
        self._badges = extralife_io.get_badges(self.badge_url)

    def _update_milestones(self) -> None:
        """Add all milestones to the list"""
        json_response = extralife_io.get_json(self.milestone_url)
        self._milestones = [Milestone.create_milestone(milestone_item) for milestone_item in json_response]

    def _update_incentives(self) -> None:
        """Add all incentives to list"""
        json_response = extralife_io.get_json(self.incentive_url)
        self._incentives = [Incentive.create_incentive(incentive) for incentive in json_response]

    def _check_existence_of_text_files(self) -> bool:
        """This is a temporary hack until I resolve Github issue #162"""
        value_in_total_raised = extralife_io.read_in_total_raised(self.text_folder)
        return value_in_total_raised != ""

    def output_donation_data(self) -> None:
        """Write out text files for donation data.

        If there have been donations, format the data (eg horizontally, vertically, etc) and output to text files.
        If there have not yet been donations, write default data to the files.
        """
        self._text_files_exist = self._check_existence_of_text_files()
        if len(self._donation_list) > 0:
            self._format_donation_information_for_output()
            self.write_text_files(self._donation_formatted_output)
            if self._top_donation is not None:
                self.write_text_files(self._top_donation_formatted_output)
        elif not self._text_files_exist:
            participant_log.info("[bold blue]No donations, writing default data to files.[/bold blue]")
            self.write_text_files(self._donation_formatted_output)

    def output_donor_data(self) -> None:
        """Write out text files for donor data.

        If there have been donations, format the data (eg horizontally, vertically, etc) and output to text files.
        If there have not yet been donations, write default data to the files.
        """
        self._text_files_exist = self._check_existence_of_text_files()
        if len(self._donation_list) > 0:
            self._format_donor_information_for_output()
            self.write_text_files(self._donor_formatted_output)
            if self._top_donor is not None:
                self.write_text_files(self._top_donor_formatted_output)
        elif not self._text_files_exist:
            participant_log.info("[bold blue]No donors or only anonymous donors, writing default data to files.[/bold "
                                 "blue]")
            self.write_text_files(self._top_donor_formatted_output)

    def output_milestone_data(self) -> None:  # pragma: no cover
        """Write out text files for Milestone data."""
        if self.milestones:
            milestone_output = {
                f"milestone_{milestone.fundraising_goal}": f"Achievement Unlocked: {milestone.description}"
                for milestone in self.milestones
                if milestone.is_complete
            }
            self.write_text_files(milestone_output)

    def output_incentive_data(self) -> None:  # pragma: no cover
        if self.incentives:
            for incentive in self.incentives:
                incentive_dictionary = {}
                incentive_folder = f"{self.text_folder}incentives/{incentive.incentive_id}"
                incentive_dictionary["amount"] = str(incentive.amount)
                incentive_dictionary["description"] = incentive.description
                incentive_dictionary["quantity"] = str(incentive.quantity)
                incentive_dictionary["quantity_claimed"] = str(incentive.quantity_claimed)
                extralife_io.write_text_files(incentive_dictionary, incentive_folder)
                if incentive.incentive_image_url:
                    html = f"<img src='{incentive.incentive_image_url}'>"
                    extralife_io.write_html_files(html, "incentive_image", incentive_folder)

    def write_text_files(self, dictionary: dict) -> None:  # pragma: no cover
        """Write OBS/XSplit display info to text files.

        It uses the helper function extralife_IO.write_text_files to handle the task.

        :param dictionary: Dictionary containing values to write to text files\
        . The key will become the filename. The value will be written to the\
        file.
        :type dictionary: dict
        """
        extralife_io.write_text_files(dictionary, self.text_folder)

    def run(self) -> None:
        """Run to get participant, donation, donor, and team data and output to text files."""
        number_of_donations = self.number_of_donations
        self.update_participant_attributes()
        self._update_incentives()
        self.output_incentive_data()
        # Below is protection against a situation where the API is unavailable.
        # Prevents bad data being written to the participant output. Based on the assumption that it would
        # absurd to have a goal of $0.
        if self.goal != 0:
            self.output_participant_data()
        if self._first_run or self.number_of_donations > number_of_donations:
            if not self._first_run:
                print("[bold green]A new donation![/bold green]")
                self._new_donation = True
            self.update_donation_data()
            self.output_donation_data()
            self.update_donor_data()
            # again, below is necessary because anonymous donors don't appear on the donor API endpoint.
            if self._donor_list:
                self.output_donor_data()
            self._update_badges()
            extralife_io.output_badge_data(self.badges, self.text_folder)
            self._update_milestones()
            self.output_milestone_data()
        # TEAM BLOCK ############################################
        if self.team_id:
            self.my_team.team_run()
        ##########################################################
        self._first_run = False
        participant_log.info("Finished checking API and updating text files!")

    def __str__(self):
        if self.my_team:
            return f"A participant with Extra Life ID {self.extralife_id}. Team info: {self.my_team}"
        else:
            return f"A participant with Extra Life ID {self.extralife_id}."


@dataclass
class Milestone:  # type: ignore
    """Fundraiser milestones associated with a Participant.

    May not be available for all instances of Donor Drive.

    More information at: https://github.com/DonorDrive/PublicAPI/blob/master/resources/milestones.md
    """
    description: str
    fundraising_goal: float
    is_active: bool
    milestone_id: str
    is_complete: bool = False
    links: dict = field(default_factory=dict)
    end_date_utc: str = ""
    start_date_utc: str = ""

    @staticmethod
    def create_milestone(json_data: dict):  # type: ignore
        """Uses the provided JSON data to create a Milestone object."""
        # let's start with the data guaranteed to be returned
        description = json_data.get("description")
        fundraising_goal = json_data.get('fundraisingGoal')
        is_active = json_data.get('isActive')
        milestone_id = json_data.get('milestoneID')
        # now the ones that may not be there
        is_complete = (
            json_data.get('isComplete') if 'isComplete' in json_data else False
        )
        links = json_data.get('links') if 'links' in json_data else {}
        end_date_utc = json_data.get('endDateUTC') if 'endDateUTC' in json_data else ''
        start_date_utc = json_data.get('startDateUTC') if 'startDateUTC' in json_data else ''
        return Milestone(description, fundraising_goal, is_active, milestone_id, is_complete, links,  # type: ignore
                         end_date_utc, start_date_utc)  # type: ignore


@dataclass
class Incentive:  # type: ignore
    """Fundraiser incentives associated with a Participant.

    May not be available for all instances of Donor Drive.

    More information at:https://github.com/DonorDrive/PublicAPI/blob/master/resources/incentives.md
    """
    amount: float
    description: str
    incentive_id: str
    is_active: str
    end_date_utc: str = ''
    incentive_image_url: str = ''
    links: dict = field(default_factory=dict)
    start_date_utc: str = ''
    quantity: int = 0
    quantity_claimed: int = 0

    @staticmethod
    def create_incentive(json_data: dict):
        """Uses the provided JSON data to create an Incentive object."""
        # guaranteed data from the API endpoint
        amount = json_data.get("amount")
        description = json_data.get("description")
        incentive_id = json_data.get('incentiveID')
        is_active = json_data.get("isActive")
        # optional data
        end_data_utc = json_data.get("endDateUTC") if "endDateUTC" in json_data else ''
        incentive_image_url = json_data.get("incentiveImageURL") if "incentiveImageURL" in json_data else ''
        links = json_data.get("links") if "links" in json_data else {}
        start_date_utc = json_data.get("startDateUTC") if "startDateUTC" in json_data else ''
        quantity = json_data.get("quantity") if "quantity" in json_data else 0
        quantity_claimed = json_data.get("quantityClaimed") if "quantityClaimed" in json_data else 0
        return Incentive(amount, description, incentive_id, is_active, end_data_utc,  # type: ignore
                         incentive_image_url, links, start_date_utc, quantity, quantity_claimed)  # type: ignore


if __name__ == "__main__":  # pragma: no cover
    participant_conf = extralife_io.ParticipantConf()
    p = Participant(participant_conf)
    while True:
        p.run()
        time.sleep(15)
