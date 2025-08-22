from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Optional

MovePath = List[Tuple[int, int]]

@dataclass
class Move:
    path: MovePath
    captures: List[Tuple[int, int]]

    @property
    def start(self) -> Tuple[int, int]:
        return self.path[0]

    @property
    def end(self) -> Tuple[int, int]:
        return self.path[-1]

class Board:
    """Represents a checkers board."""

    def __init__(self):
        self.board = self._create_initial_board()

    def _create_initial_board(self):
        board: List[List[Optional[str]]] = [[None] * 8 for _ in range(8)]
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'b'
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'r'
        return board

    def clone(self) -> 'Board':
        new = Board()
        new.board = [row[:] for row in self.board]
        return new

    def get_piece(self, row: int, col: int) -> Optional[str]:
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None

    def set_piece(self, row: int, col: int, piece: Optional[str]):
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = piece

    @staticmethod
    def opponent(color: str) -> str:
        return 'b' if color == 'r' else 'r'

    def _get_directions(self, piece: str) -> List[Tuple[int, int]]:
        if piece == 'r':
            return [(-1, -1), (-1, 1)]
        if piece == 'b':
            return [(1, -1), (1, 1)]
        return [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    def get_legal_moves(self, color: str) -> List[Move]:
        captures: List[Move] = []
        moves: List[Move] = []
        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece and piece.lower() == color:
                    captures.extend(self._piece_captures(r, c, piece))
        if captures:
            return captures
        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece and piece.lower() == color:
                    moves.extend(self._piece_simple_moves(r, c, piece))
        return moves

    def _piece_simple_moves(self, row: int, col: int, piece: str) -> List[Move]:
        result: List[Move] = []
        for dr, dc in self._get_directions(piece):
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.get_piece(r, c) is None:
                result.append(Move([(row, col), (r, c)], []))
        return result

    def _piece_captures(self, row: int, col: int, piece: str,
                        path: Optional[MovePath] = None,
                        captures: Optional[List[Tuple[int, int]]] = None) -> List[Move]:
        if path is None:
            path = [(row, col)]
        if captures is None:
            captures = []
        result: List[Move] = []
        has_capture = False
        for dr, dc in self._get_directions(piece):
            mid_r, mid_c = row + dr, col + dc
            end_r, end_c = row + 2 * dr, col + 2 * dc
            if (
                0 <= end_r < 8 and 0 <= end_c < 8 and
                self.get_piece(mid_r, mid_c) and
                self.get_piece(mid_r, mid_c).lower() == Board.opponent(piece.lower()) and
                self.get_piece(end_r, end_c) is None
            ):
                has_capture = True
                temp_piece = self.get_piece(row, col)
                captured_piece = self.get_piece(mid_r, mid_c)
                self.set_piece(row, col, None)
                self.set_piece(mid_r, mid_c, None)
                self.set_piece(end_r, end_c, temp_piece)
                result.extend(self._piece_captures(
                    end_r, end_c, temp_piece,
                    path + [(end_r, end_c)],
                    captures + [(mid_r, mid_c)]
                ))
                self.set_piece(row, col, temp_piece)
                self.set_piece(mid_r, mid_c, captured_piece)
                self.set_piece(end_r, end_c, None)
        if not has_capture and len(path) > 1:
            result.append(Move(path, captures))
        return result

    def apply_move(self, move: Move):
        for i in range(len(move.path) - 1):
            r1, c1 = move.path[i]
            r2, c2 = move.path[i + 1]
            piece = self.get_piece(r1, c1)
            self.set_piece(r1, c1, None)
            self.set_piece(r2, c2, piece)
        for r, c in move.captures:
            self.set_piece(r, c, None)
        end_r, end_c = move.end
        piece = self.get_piece(end_r, end_c)
        if piece == 'r' and end_r == 0:
            self.set_piece(end_r, end_c, 'R')
        if piece == 'b' and end_r == 7:
            self.set_piece(end_r, end_c, 'B')

    def is_game_over(self) -> bool:
        return not self.get_legal_moves('r') or not self.get_legal_moves('b')

    def winner(self) -> Optional[str]:
        if self.get_legal_moves('r') and not self.get_legal_moves('b'):
            return 'r'
        if self.get_legal_moves('b') and not self.get_legal_moves('r'):
            return 'b'
        return None

    def evaluate(self, color: str) -> float:
        score = 0.0
        for row in self.board:
            for piece in row:
                if piece:
                    val = 1.0
                    if piece.isupper():
                        val = 1.5
                    if piece.lower() == color:
                        score += val
                    else:
                        score -= val
        return score
