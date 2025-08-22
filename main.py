from __future__ import annotations

from pathlib import Path

from checkers.game import Game
from checkers.history import History
from checkers.points import Points

LEVEL_FILE = Path('level.txt')


def get_level() -> int:
    if LEVEL_FILE.exists():
        return int(LEVEL_FILE.read_text())
    LEVEL_FILE.write_text('1')
    return 1


def set_level(level: int):
    LEVEL_FILE.write_text(str(level))


def main():
    level = get_level()
    depth_map = {1: 2, 2: 4, 3: 6}
    game = Game(ai_depth=depth_map.get(level, 2))
    winner = game.play()
    if winner == 'r' and level < 3:
        set_level(level + 1)
        print(f"Level up! New level: {level + 1}")
    history = History().stats()
    points = Points().stats()
    print("Winner:", winner)
    print("Stats:", history['wins'], "wins,", history['losses'], "losses")
    print("Points:", points['points'])
    print("Unlocked skins:", ', '.join(points['skins']) or 'none')


if __name__ == '__main__':
    main()
