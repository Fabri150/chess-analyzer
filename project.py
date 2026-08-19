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
                return "tie"
        else:
            if self.result == "1-0":
                return "lose"
            elif self.result == "0-1":
                return "win"
            else:
                return "tie"