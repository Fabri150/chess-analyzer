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

    def opening_rates(self, min_played= 3):
        rates = {}
        for opening, results in self.opening_results().items():
            if opening == "Unknown" or (sum(results.values()) < min_played):
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

def main():
    user = input("What's your Lichess username?: ")
    #pgn_matches = input("Insert your API URL here: ")
    with open(...) as f:
        pgn = f.read()
    a = Analyzer(user)
    a.load_matches(pgn)
    #print(a.analyzer_results())
    #print(a.match_rates())
    #print(a.color_results())
    #print(a.color_rates())
    print(a.opening_results())
    print(a.opening_rates(1))

if __name__ == "__main__":
    main()