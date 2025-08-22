from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from .board import Board, Move
from .ai import minimax


def display_board(board: Board):
    for r in range(8):
        row = []
        for c in range(8):
            piece = board.get_piece(r, c)
            row.append(piece if piece else '.')
        print(r, ' '.join(row))
    print('  0 1 2 3 4 5 6 7')


class HumanPlayer:
    color = 'r'

    def get_move(self, board: Board) -> Move:
        moves = board.get_legal_moves(self.color)
        while True:
            display_board(board)
            raw = input("Enter move as 'r1 c1 r2 c2 [r3 c3 ...]': ")
            try:
                nums = list(map(int, raw.split()))
                path = list(zip(nums[::2], nums[1::2]))
                for mv in moves:
                    if mv.path == path:
                        return mv
            except Exception:
                pass
            print("Invalid move. Try again.")


@dataclass
class AIPlayer:
    color: str
    depth: int

    def get_move(self, board: Board) -> Move:
        _, move = minimax(board, self.depth, self.color, True)
        assert move is not None
        return move
