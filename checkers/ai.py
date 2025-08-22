from __future__ import annotations

from typing import Tuple
from math import inf

from .board import Board, Move


def minimax(board: Board, depth: int, color: str, maximizing: bool) -> Tuple[float, Move | None]:
    if depth == 0 or board.is_game_over():
        return board.evaluate(color), None

    moves = board.get_legal_moves(color if maximizing else Board.opponent(color))
    best_move = None
    if maximizing:
        best_val = -inf
        for move in moves:
            new_board = board.clone()
            new_board.apply_move(move)
            val, _ = minimax(new_board, depth - 1, color, False)
            if val > best_val:
                best_val = val
                best_move = move
        return best_val, best_move
    else:
        best_val = inf
        for move in moves:
            new_board = board.clone()
            new_board.apply_move(move)
            val, _ = minimax(new_board, depth - 1, color, True)
            if val < best_val:
                best_val = val
                best_move = move
        return best_val, best_move
