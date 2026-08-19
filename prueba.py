import chess.pgn

pgn = open("data/pgn/kasparov-deep-blue-1997.pgn")

first_game = chess.pgn.read_game(pgn)