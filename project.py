import chess.pgn
import io

class Match:
    def __init__(self, user, result, white_player, black_player):
        self.user = user
        self.result = result
        self.white_player = white_player
        self.black_player = black_player

    @classmethod
    def from_pgn(cls, headers, user):
        result = headers["Result"]
        white = headers["White"]
        black = headers["Black"]
        return cls(user, result, white, black)

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

    def rates(self):
        if len(self.matches) == 0:
            return {"winrate": 0, "lossrate": 0, "drawrate": 0}
        
        results = self.analyzer_results()
        return {"winrate": round(results['win'] / len(self.matches) * 100, 2),
                "lossrate": round(results['lose'] / len(self.matches) * 100, 2),
                "drawrate": round(results['draw'] / len(self.matches) * 100, 2)}

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
    with open("lichess_Fabri150_2026-08-19.pgn") as f:
        pgn = f.read()
    a = Analyzer(user)
    a.load_matches(pgn)
    print(a.analyzer_results())
    print(a.rates())

if __name__ == "__main__":
    main()