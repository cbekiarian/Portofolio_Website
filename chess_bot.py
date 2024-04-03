import chess
from stockfish import Stockfish

class ChessBot():
    def __init__(self):
        self.board = chess.Board()
        self.stockfish = Stockfish("stockfish-windows-x86-64-avx2.exe")
        self.stockfish.set_depth(20)
        self.stockfish.set_skill_level(20)
        self.color = "Black"

    def player_move(self):
        self.board.push_san('')
        self.stockfish.set_fen_position(self.board.fen())
        d = self.stockfish.get_top_moves(1)[0]["Move"]
        print(d)
        self.board.push_san(d)
        print(self.board.fen())
        print(self.board)

    def reset(self):
        self.board = chess.Board()
        return


pog = ChessBot()
pog.player_move()