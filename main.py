import argparse
from tabulate import tabulate
import sys

from src import elo

# Add the tournaments you want to scan here if you are not scanning all
TOURNAMENTS_TO_SCAN = {
    "the-big-deal-3d": "startgg",
    "ceo-2019-fighting-game-championships": "startgg",
}


def parse_args():
    parser = argparse.ArgumentParser(description="Get Elo ratings of players")
    parser.add_argument(
        "--all", help="Lookup all DDR tournaments possible", action="store_true"
    )
    parser.add_argument(
        "--count",
        "-c",
        help="Only show players with a minimum number of plays",
        default=0,
    )

    args = parser.parse_args()
    if int(args.count) < 0:
        print("ERROR: Count must be greater than 0")
        parser.print_help()
        sys.exit(5)
    return args


def main():
    args = parse_args()

    players = elo.Players()
    matches = elo.Matches()

    if args.all:
        print("Getting brackets from all available tournaments from start.gg")
        brackets = elo.get_all_brackets()
        print("Getting all available players in tournaments")
        elo.add_players(list(set(brackets)), players)
        print("Getting all matches")
        print("NOTE: This will take a while")
        elo.add_matches(list(set(brackets)), players, matches)
    else:
        for tournament, location in TOURNAMENTS_TO_SCAN.items():
            print(f"Getting brackets from tournament {tournament}")
            brackets = elo.get_brackets(tournament, location)
            print(f"Getting players from {tournament}")
            elo.add_players(brackets, players)
            print(f"Getting matches from {tournament}")
            elo.add_matches(brackets, players, matches)

    # Assuming match IDs are roughly chronological
    matches.matches = sorted(matches.matches, key=lambda m: m.id)

    print(f"Adjusting ratings of {len(players)} players")
    for match in matches.matches:
        elo.adjust_player_ratings_from_match(match)

    print("\nElo ratings of all players:\n")

    filtered_player_list = []
    if args.count:
        for player in players.players:
            if player.get_total_matches() > int(args.count):
                filtered_player_list.append(player)
    else:
        filtered_player_list = players.players

    table = [
        [
            rank,
            player.name,
            round(player.rating),
            (
                f"{player.wins}-{player.losses}-{player.draws} "
                f"({player.get_record_percentage()}%)"
            ),
        ]
        for rank, player in enumerate(
            sorted(filtered_player_list, key=lambda p: p.rating, reverse=True),
            start=1,
        )
    ]
    print(tabulate(table, headers=["Rank", "Name", "Rating", "Record"]))


if "__main__" in __name__:
    main()
