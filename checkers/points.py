from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any


class Points:
    def __init__(self, path: str | Path = 'points.json'):
        self.path = Path(path)
        if not self.path.exists():
            self._save({'points': 0, 'skins': []})

    def _load(self) -> Dict[str, Any]:
        return json.loads(self.path.read_text())

    def _save(self, data: Dict[str, Any]):
        self.path.write_text(json.dumps(data, indent=2))

    def add_points(self, value: int):
        data = self._load()
        data['points'] += value
        self._save(data)

    def check_unlocks(self):
        data = self._load()
        skins = data['skins']
        for skin, cost in [('wood', 50), ('metal', 100)]:
            if data['points'] >= cost and skin not in skins:
                skins.append(skin)
        self._save(data)

    def stats(self) -> Dict[str, Any]:
        return self._load()
