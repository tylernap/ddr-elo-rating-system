from dataclasses import dataclass
import logging
import os
import sys

import dotenv
import pysmashgg

dotenv.load_dotenv()
API_TOKEN = os.getenv("STARTGG_API_TOKEN")
smash = pysmashgg.SmashGG(API_TOKEN, True)


def get_brackets_from_tournament(tournament_name: str) -> list:
    events = smash.tournament_show_all_event_brackets(tournament_name)
    brackets = []
    for event in events:
        if (
            "DanceDanceRevolution" in event["eventName"]
            or "Dance Dance Revolution" in event["eventName"]
        ):
            brackets += event["bracketIds"]

    return brackets


def get_players_from_bracket(bracket: str) -> list:
    entrants = []
    page_number = 1
    while True:
        page = smash.bracket_show_entrants(bracket, page_number)
        if not page:
            break
        entrants += page
        page_number += 1

    return entrants


def get_matches_from_bracket(bracket: str) -> list:
    matches = []
    page_number = 1
    while True:
        page = smash.bracket_show_sets(bracket, page_number)
        if not page:
            break
        matches += page
        page_number += 1

    return matches
