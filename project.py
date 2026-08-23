import chess.pgn
import io

class Match:
    def __init__(self, user, result, white_player, black_player, eco, opening):
        self.user = user
        self.result = result
        self.white_player = white_player
        self.black_player = black_player
        self.eco = eco
        self.opening = opening

    @classmethod
    def from_pgn(cls, headers, user):
        result = headers["Result"]
        white = headers["White"]
        black = headers["Black"]
        eco = headers.get("ECO", "Unknown")
        opening = headers.get("Opening", "Unknown")
        return cls(user, result, white, black, eco, opening)

    def my_color(self):
        if self.white_player == self.user:
            return "white"
        elif self.black_player == self.user:
            return "black"
        else:
            raise ValueError(f"User {self.user} not found")

    def result_match(self):
        if self.result not in ("1-0", "0-1", "1/2-1/2"):
            raise ValueError(f"{self.result} is an invalid result")

        color = self.my_color()
        if color == "white":
            if self.result == "1-0":
                return "win"
            elif self.result == "0-1":
                return "lose"
            else:
                return "draw"
        else:
            if self.result == "1-0":
                return "lose"
            elif self.result == "0-1":
                return "win"
            else:
                return "draw"

class Analyzer:
    def __init__(self, user):
        self.user = user
        self.matches = []

    def analyzer_results(self):
        results = {"win": 0, "lose": 0, "draw": 0}
        for match in self.matches:
            result = match.result_match()
            if result == "win":
                results["win"] += 1
            elif result == "lose":
                results["lose"] += 1
            else:
                results["draw"] += 1
        return results

    def calculate_rates(self, results_dict):
        total = sum(results_dict.values())
        if total == 0:
            return {"winrate": 0, "loserate": 0, "drawrate": 0}
        return {
            "winrate": round(results_dict["win"] / total * 100, 2),
            "loserate": round(results_dict["lose"] / total * 100, 2),
            "drawrate": round(results_dict["draw"] / total * 100, 2)
        }

    def match_rates(self):
        return self.calculate_rates(self.analyzer_results())

    def color_results(self):
        results = {"white": {"win": 0, "lose": 0, "draw": 0}, 
                "black": {"win": 0, "lose": 0, "draw": 0}}
        
        for match in self.matches:
            color = match.my_color()
            result = match.result_match()
            results[color][result] += 1
        return results

    def color_rates(self):
        results = self.color_results()

        white_rates = self.calculate_rates(results["white"])
        black_rates = self.calculate_rates(results["black"])

        return {"white": white_rates, "black": black_rates}

    def opening_results(self):
        results = {}
        for match in self.matches:
            opening = match.opening
            results.setdefault(opening, {"win": 0, "lose": 0, "draw": 0})
            result = match.result_match()
            results[opening][result] += 1
        return results

    def opening_rates(self):
        rates = {}
        for opening, results in self.opening_results().items():
            if opening == "Unknown":
                continue
            rates.update({opening: self.calculate_rates(results)})
        return rates

    def load_matches(self, pgn):
        pgn_io = io.StringIO(pgn)
        game = chess.pgn.read_game(pgn_io)
        while game is not None:
            match = Match.from_pgn(game.headers, self.user)
            self.matches.append(match)
            game = chess.pgn.read_game(pgn_io)

    def print_report(self):
        match_rates = self.match_rates()
        analyzer_results = self.analyzer_results()
        color_rates = self.color_rates()
        color_results = self.color_results()
        openings_for_sort = self.opening_results()
        opening_rates = self.opening_rates()

        openings_sorted = sorted(openings_for_sort, key=lambda opening: sum(openings_for_sort[opening].values()), reverse=True)
        top_10 = [opening for opening in openings_sorted if opening != "Unknown"][:10]

        openings = []
        for opening in top_10:
            openings.append(f"""Name: {opening}
Total Matches: {sum(openings_for_sort[opening].values())}
Winrate: {opening_rates[opening]["winrate"]} ({openings_for_sort[opening]["win"]} wins)
Drawrate: {opening_rates[opening]["drawrate"]} ({openings_for_sort[opening]["draw"]} draws)
Loserate: {opening_rates[opening]["loserate"]} ({openings_for_sort[opening]["lose"]} loses)""")
        openings_text = "\n\n".join(openings)

        return f"""
Stats of {self.user}:
Total matches: {sum(self.analyzer_results().values())}
Winrate: {match_rates["winrate"]} ({analyzer_results["win"]} wins)
Drawrate: {match_rates["drawrate"]} ({analyzer_results["draw"]} draws)
Loserate: {match_rates["loserate"]} ({analyzer_results["lose"]} loses)

Matches with white: {sum(color_results["white"].values())}
Winrate: {color_rates["white"]["winrate"]} ({color_results["white"]["win"]} wins)
Drawrate: {color_rates["white"]["drawrate"]} ({color_results["white"]["draw"]} draws)
Loserate: {color_rates["white"]["loserate"]} ({color_results["white"]["lose"]} loses)

Matches with black: {sum(color_results["black"].values())}
Winrate: {color_rates["black"]["winrate"]} ({color_results["black"]["win"]} wins)
Drawrate: {color_rates["black"]["drawrate"]} ({color_results["black"]["draw"]} draws)
Loserate: {color_rates["black"]["loserate"]} ({color_results["black"]["lose"]} loses)

Stats with openings:
{openings_text}
"""

def main():
    user = input("What's your Lichess username?: ")
    #pgn_matches = input("Insert your API URL here: ")
    with open("lichess_Fabri150_2026-08-21.pgn") as f:
        pgn = f.read()
    a = Analyzer(user)
    a.load_matches(pgn)
    if not a.matches:
        print("No matches found for this user.")
    else:
        print(a.print_report())

if __name__ == "__main__":
    main()