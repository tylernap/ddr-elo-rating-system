from tabulate import tabulate

from src import elo

TOURNAMENTS_TO_SCAN = {
    "the-big-deal-3d": "startgg",
    "ceo-2019-fighting-game-championships": "startgg",
    "infinity-stage-san-jose": "startgg",
    "mistake-on-the-lake-3": "startgg",
}


def main():
    players = elo.Players()
    matches = elo.Matches()
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
    table = [
        [player.name, round(player.rating)]
        for player in sorted(players.players, key=lambda p: p.rating, reverse=True)
    ]
    print(tabulate(table, headers=["Name", "Rating"]))


if "__main__" in __name__:
    main()
