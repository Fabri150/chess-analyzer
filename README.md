# Chess Match Analyzer

Python chess game analyzer for Lichess games — connects to the Lichess API, downloads a user's games, and generates a statistical report covering overall performance, performance by color, and the most played openings.

## Description

Chess Match Analyzer is a command-line tool that fetches a Lichess player's games directly from the Lichess API, parses them, and produces a report with three levels of analysis:

- **Overall stats**: total matches, win/loss/draw rate.
- **Stats by color**: win/loss/draw rate broken down between games played as white and as black.
- **Opening stats**: the 10 most-played openings, each with its own win/loss/draw rate — similar to how chess.com presents opening performance.

The user is prompted for a Lichess username and how many recent games to analyze, then the tool handles fetching, parsing, and reporting automatically.

## Project Structure

- **`project.py`** — Contains all the core logic:
  - `Match`: represents a single chess game, parsed from PGN headers. Determines the user's color and the game's outcome from the user's perspective.
  - `Analyzer`: loads a user's games and calculates statistics at the overall, color, and opening level. Also generates the final formatted report.
  - `get_matches()`: fetches PGN data for a given user directly from the Lichess API.
  - `main()`: handles user input, error cases (invalid input, user not found, rate limiting), and ties everything together.
- **`test_project.py`** — Unit tests (via `pytest`) for `my_color()`, `result_match()`, and `calculate_rates()`, covering both expected outputs and error cases.
- **`requirements.txt`** — External dependencies needed to run the project (`requests`, `chess`).

## Installation & Usage

1. Clone this repository.
2. Install the dependencies:
pip install -r requirements.txt
3. Run the program:
python project.py
4. Enter a valid Lichess username and the number of recent games you'd like to analyze.

## Design Notes

- **Opening analysis approach**: an early version tried to determine a single "best" and "worst" opening using a minimum-games threshold to filter out unreliable small samples. This proved fragile — with few games, the same opening could end up ranked as both best and worst. The design was changed to show the top 10 most-played openings instead (similar to chess.com), letting the user compare openings directly rather than forcing a single winner/loser from limited data.
- **Separation of calculation and presentation**: methods that calculate statistics (e.g. `analyzer_results()`, `calculate_rates()`) never print or raise user-facing messages — they always return predictable data structures. User communication (e.g. "no matches found", "user not found") is handled separately in `main()`, keeping the analysis logic reusable and easy to test.

## Future Improvements

- Filter analysis by time control (bullet, blitz, rapid, classical).
- Group openings by family (e.g. treat all Caro-Kann variations as one) rather than by exact name.
- Allow analyzing games of any Lichess user, not just the person running the tool.
- Visualize stats (e.g. with `matplotlib`) instead of a text-only report.
