from __future__ import annotations

import json
import datetime as dt
from pathlib import Path
from typing import Dict, Any, List


class History:
    def __init__(self, path: str | Path = 'history.json'):
        self.path = Path(path)
        if not self.path.exists():
            self._save([])

    def _load(self) -> List[Dict[str, Any]]:
        return json.loads(self.path.read_text())

    def _save(self, data: List[Dict[str, Any]]):
        self.path.write_text(json.dumps(data, indent=2))

    def record(self, result: str, points: int):
        data = self._load()
        data.append({
            'timestamp': dt.datetime.utcnow().isoformat(),
            'result': result,
            'points': points,
        })
        self._save(data)

    def stats(self) -> Dict[str, Any]:
        data = self._load()
        wins = sum(1 for d in data if d['result'] == 'win')
        losses = sum(1 for d in data if d['result'] == 'loss')
        total = sum(d['points'] for d in data)
        return {
            'wins': wins,
            'losses': losses,
            'points': total,
            'history': data,
        }
