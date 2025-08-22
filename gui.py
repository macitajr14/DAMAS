from __future__ import annotations

from pathlib import Path
from tkinter import Canvas, Tk, messagebox

from checkers.board import Board, Move
from checkers.player import AIPlayer
from checkers.history import History
from checkers.points import Points

SQUARE_SIZE = 60
LEVEL_FILE = Path('level.txt')


def get_level() -> int:
    if LEVEL_FILE.exists():
        return int(LEVEL_FILE.read_text())
    LEVEL_FILE.write_text('1')
    return 1


def set_level(level: int):
    LEVEL_FILE.write_text(str(level))


class GameGUI:
    """Simple Tkinter GUI for playing checkers against the AI."""

    def __init__(self) -> None:
        level = get_level()
        depth_map = {1: 2, 2: 4, 3: 6}
        self.board = Board()
        self.ai = AIPlayer('b', depth_map.get(level, 2))
        self.turn = 'r'
        self.history = History()
        self.points = Points()
        self.selected: tuple[int, int] | None = None
        self.moves: list[Move] = []

        self.root = Tk()
        self.root.title('Checkers')
        size = SQUARE_SIZE * 8
        self.canvas = Canvas(self.root, width=size, height=size)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.on_click)
        self.draw_board()

    # --- drawing -----------------------------------------------------
    def draw_board(self) -> None:
        self.canvas.delete('all')
        for r in range(8):
            for c in range(8):
                x1, y1 = c * SQUARE_SIZE, r * SQUARE_SIZE
                x2, y2 = x1 + SQUARE_SIZE, y1 + SQUARE_SIZE
                color = '#D18B47' if (r + c) % 2 else '#FFCE9E'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')
                piece = self.board.get_piece(r, c)
                if piece:
                    fill = 'red' if piece.lower() == 'r' else 'black'
                    self.canvas.create_oval(
                        x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=fill, outline='white'
                    )
                    if piece.isupper():
                        self.canvas.create_text(
                            (x1 + x2) / 2,
                            (y1 + y2) / 2,
                            text='K',
                            fill='white',
                        )
        if self.selected:
            sr, sc = self.selected
            x1, y1 = sc * SQUARE_SIZE, sr * SQUARE_SIZE
            x2, y2 = x1 + SQUARE_SIZE, y1 + SQUARE_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, outline='yellow', width=3)
            for mv in self.moves:
                er, ec = mv.end
                x1, y1 = ec * SQUARE_SIZE, er * SQUARE_SIZE
                x2, y2 = x1 + SQUARE_SIZE, y1 + SQUARE_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, outline='green', width=3)

    # --- game logic --------------------------------------------------
    def on_click(self, event) -> None:
        if self.turn != 'r':
            return
        r = event.y // SQUARE_SIZE
        c = event.x // SQUARE_SIZE
        if self.selected:
            for mv in self.moves:
                if mv.end == (r, c):
                    self.board.apply_move(mv)
                    self.turn = 'b'
                    self.selected = None
                    self.moves = []
                    self.draw_board()
                    self.root.after(300, self.ai_move)
                    self.check_game_over()
                    return
        piece = self.board.get_piece(r, c)
        if piece and piece.lower() == 'r':
            self.selected = (r, c)
            all_moves = self.board.get_legal_moves('r')
            self.moves = [m for m in all_moves if m.start == (r, c)]
            self.draw_board()

    def ai_move(self) -> None:
        if self.board.is_game_over():
            self.check_game_over()
            return
        move = self.ai.get_move(self.board)
        self.board.apply_move(move)
        self.turn = 'r'
        self.draw_board()
        self.check_game_over()

    def check_game_over(self) -> None:
        if not self.board.is_game_over():
            return
        winner = self.board.winner()
        message = 'You lose!'
        if winner == 'r':
            message = 'You win!'
            self.points.add_points(10)
            self.points.check_unlocks()
            self.history.record('win', 10)
            level = get_level()
            if level < 3:
                set_level(level + 1)
                message += f" Level up! New level: {level + 1}"
        else:
            self.history.record('loss', 0)
        messagebox.showinfo('Game Over', message)
        self.root.quit()

    def run(self) -> None:
        self.root.mainloop()


if __name__ == '__main__':
    GameGUI().run()
