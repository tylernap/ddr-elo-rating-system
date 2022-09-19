from dataclasses import dataclass
import logging
import os
import sys
import time
from typing import Callable

import dotenv
import pysmashgg

dotenv.load_dotenv()
API_TOKEN = os.getenv("STARTGG_API_TOKEN")
smash = pysmashgg.SmashGG(API_TOKEN, True)

# TODO: These game IDs were obtained manually through a graphql query to start.gg
# This could probably be automated at some point, but for now...
DDR_A_ID = 2902
DDR_A20_ID = 33637
DDR_EXTREME_PRO_ID = 2907

# Filter all tournaments by minimum number of entrants
MIN_NUM_OF_ENTRANTS = 20

# Include these tournaments
NAME_INCLUDE_FILTER = ["Dance Dance Revolution", "DanceDanceRevolution", "DDR"]
# Exclude these tournaments
NAME_EXCLUDE_FILTER = ["Freestyle", "freestyle"]


def paginate(function: Callable, *args) -> list:
    """
    A helper function to help us paginate through start.gg responses
    """
    results = []
    page_number = 1
    while True:
        try:
            page = function(*args, page_number)
            if not page:
                return results
            results += page
        except TypeError as e:
            print(f"Failed to return results: {str(e)}")
        page_number += 1


def get_brackets_from_all_tournaments() -> list:
    tournaments = []
    # Get tournaments for DDR A
    tournaments += paginate(
        smash.tournament_show_event_by_game_size_dated,
        MIN_NUM_OF_ENTRANTS,
        DDR_A_ID,
        0,
        int(time.time()),
    )

    # Get tournaments for DDR A20
    tournaments += paginate(
        smash.tournament_show_event_by_game_size_dated,
        MIN_NUM_OF_ENTRANTS,
        DDR_A20_ID,
        0,
        int(time.time()),
    )

    # Get tournaments for DDR Extreme Pro
    tournaments += paginate(
        smash.tournament_show_event_by_game_size_dated,
        MIN_NUM_OF_ENTRANTS,
        DDR_EXTREME_PRO_ID,
        0,
        int(time.time()),
    )

    brackets = []
    for tournament in tournaments:
        brackets += get_brackets_from_tournament(tournament["tournamentSlug"])

    return brackets


def get_brackets_from_tournament(tournament_name: str) -> list:
    events = smash.tournament_show_all_event_brackets(tournament_name)
    brackets = []
    for event in events:
        if any(x in event["eventName"] for x in NAME_INCLUDE_FILTER) and not any(
            x in event["eventName"] for x in NAME_EXCLUDE_FILTER
        ):
            brackets += event["bracketIds"]

    return brackets


def get_players_from_bracket(bracket: str) -> list:
    return paginate(smash.bracket_show_entrants, bracket)


def get_matches_from_bracket(bracket: str) -> list:
    return paginate(smash.bracket_show_sets, bracket)
