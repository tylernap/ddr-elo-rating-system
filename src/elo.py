from dataclasses import dataclass
import logging
import math

from src import startgg

K_FACTOR = 32
SCALE_FACTOR = 400

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@dataclass
class Player:
    """
    Class to keep track of player data
    """

    name: str
    id: str
    rating: int = 1000
    wins: int = 0
    losses: int = 0
    draws: int = 0

    def get_total_matches(self):
        return self.wins + self.losses + self.draws

    def get_record_percentage(self):
        return int(100 * ((self.wins + self.draws / 2) / (self.get_total_matches())))


class Players:
    """
    List object that keeps track of players
    """

    def __init__(self):
        self.players = []

    def __len__(self):
        return len(self.players)

    def get_player(self, id: str):
        for player in self.players:
            if player.id == id:
                return player
        return None

    def add_player(self, new_player: Player):
        for player in self.players:
            if player.name == new_player.name:
                logger.warning(f"Player {new_player.name} already exists")
                return
        logger.info(f"Creating new player {new_player.name}")
        self.players.append(new_player)


@dataclass
class Match:
    """
    Class to keep track of match data
    """

    id: str
    player1: Player
    player2: Player
    complete: bool
    player1_score: int
    player2_score: int


class Matches:
    """
    List object that keeps track of matches
    """

    def __init__(self):
        self.matches = []

    def __len__(self):
        return len(self.matches)

    def get_match(self, id: str):
        for match in self.matches:
            if match.id == id:
                return match
        return None

    def add_match(self, new_match: Match):
        for match in self.matches:
            if match.id == new_match.id:
                logger.warning(f"Match ID {new_match.id} already exists")
                return
        logger.info(f"Adding new match {new_match.id}")
        self.matches.append(new_match)


def get_all_brackets():
    brackets = []
    brackets += startgg.get_brackets_from_all_tournaments()
    return brackets


def get_brackets(tournament: str, location: str):
    if location == "startgg":
        return startgg.get_brackets_from_tournament(tournament)


def add_players(brackets: list, players: Players):
    for bracket in brackets:
        entrants = startgg.get_players_from_bracket(bracket)
        for entrant in entrants:
            id = entrant["entrantPlayers"][0]["playerId"]
            name = entrant["entrantPlayers"][0]["playerTag"]
            player = Player(name, id)
            players.add_player(player)


def add_matches(brackets: list, players: Players, matches: Matches):
    for bracket in brackets:
        for startgg_match in startgg.get_matches_from_bracket(bracket):
            if not startgg_match["completed"]:
                logger.info(f"Match {startgg_match} is not complete. Skipping")
                continue
            match = Match(
                startgg_match["id"],
                players.get_player(startgg_match["entrant1Players"][0]["playerId"]),
                players.get_player(startgg_match["entrant2Players"][0]["playerId"]),
                startgg_match["completed"],
                startgg_match["entrant1Score"],
                startgg_match["entrant2Score"],
            )
            matches.add_match(match)


def adjust_player_ratings_from_match(match: Match):
    if match.player1 is None or match.player2 is None:
        logger.warning(f"Could not find players of match {match.id}")
        return
    player1_expected_score = 1 / (
        1 + math.pow(10, (match.player2.rating - match.player1.rating) / SCALE_FACTOR)
    )
    player2_expected_score = 1 / (
        1 + math.pow(10, (match.player1.rating - match.player2.rating) / SCALE_FACTOR)
    )

    if match.player1_score > match.player2_score:
        match.player1.rating = match.player1.rating + (
            K_FACTOR * (1 - player1_expected_score)
        )
        match.player2.rating = match.player2.rating + (
            K_FACTOR * (0 - player2_expected_score)
        )
        match.player1.wins += 1
        match.player2.losses += 1
    elif match.player1_score < match.player2_score:
        match.player1.rating = match.player1.rating + (
            K_FACTOR * (0 - player1_expected_score)
        )
        match.player2.rating = match.player2.rating + (
            K_FACTOR * (1 - player2_expected_score)
        )
        match.player1.losses += 1
        match.player2.wins += 1
    # Ideally, this should never happen, but adding it anyway just in case
    elif match.player1_score == match.player2_score:
        match.player1.rating = match.player1.rating + (
            K_FACTOR * (0.5 - player1_expected_score)
        )
        match.player2.rating = match.player2.rating + (
            K_FACTOR * (0.5 - player2_expected_score)
        )
        match.player1.draws += 1
        match.player2.draws += 1
