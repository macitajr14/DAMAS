from __future__ import annotations

from .board import Board
from .player import HumanPlayer, AIPlayer
from .history import History
from .points import Points


class Game:
    def __init__(self, ai_depth: int = 2):
        self.board = Board()
        self.human = HumanPlayer()
        self.ai = AIPlayer('b', ai_depth)
        self.turn = 'r'
        self.history = History()
        self.points = Points()

    def play(self) -> str | None:
        while not self.board.is_game_over():
            if self.turn == 'r':
                move = self.human.get_move(self.board)
            else:
                move = self.ai.get_move(self.board)
            self.board.apply_move(move)
            self.turn = Board.opponent(self.turn)
        winner = self.board.winner()
        if winner == 'r':
            self.points.add_points(10)
            self.points.check_unlocks()
            self.history.record('win', 10)
        else:
            self.history.record('loss', 0)
        return winner
