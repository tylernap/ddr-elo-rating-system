# ddr-elo-rating-system
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A small application to help calculate Elo ratings of DDR Players based on past performances

```
Adjusting ratings of 573 players

Elo ratings of all players:

Name                      Rating
----------------------  --------
bob                         1318
phil                        1207
kevin                       1176
chris                       1133
...
```

## Usage
```
usage: main.py [-h] [--all] [--count COUNT]

Get Elo ratings of players

optional arguments:
  -h, --help            show this help message and exit
  --all                 Lookup all DDR tournaments possible
  --count COUNT, -c COUNT
                        Only show players with a minimum number of plays
```

## Why?
This is mainly a pet project that I started to help standardize the skills of players within tournament settings. The hope is that this or something like this can be used in a more widespread way.

## The Math
If you are interested in looking up how an Elo ranking is implemented, check out [this article from Medium about how Elo works](https://medium.com/purple-theory/what-is-elo-rating-c4eb7a9061e0). For now, the calculations are basic using a static K-factor value of 32 and a rating scale of 400.

## API Tokens
In order to use this, you will need an API token from the various locations to pull data. See the following for how to obtain them:
- [smash.gg](https://developer.start.gg/docs/authentication)

The API tokens are read in via environment variables or your `.env` file. To use the `.env` file, copy `env.example` to `.env` and then simply insert your API token where designated.

## Choosing tournaments
In `main.py` there is a variable called `TOURNAMENTS_TO_SCAN`. Add the name of the tournament you wish you scan as well as the location of said tournament. See #supported-locations for supported locations and more information.

You can get the name of the tournament by looking at the URL of the event. For instance, with a url of `https://www.start.gg/tournament/this-is-my-tournament/events` you can see that the name of the tournament is `this-is-my-tournament`.

If you want to scan everything, use the `--all` argument when running `main.py`. This will ignore the specificed tournaments and instead look for all tournaments running the games in `GAMES_TO_SEARCH` in `startgg.py`.

## Supported locations
These are the currently supported tournament bracket locations. Expect to see more in the future:
- [startgg](https://www.start.gg)

## Room for Improvement
- Add unit testing
- Scale this out to a larger application rather than a script
- Pull already existing ratings from an external source
- Add varying K-factors based on how we see the distribution of players

## Development
If you would like to contribute to the project, feel free to open up PRs. Everything is stylized and linted using [black](https://github.com/psf/black).
