"""Load, validate and analyse a risk register."""
from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path
from .model import Risk, rating


class Register:
    def __init__(self, risks: list[Risk], appetite: float = 10.0):
        self.risks = risks
        self.appetite = appetite  # residual score above this breaches appetite

    @classmethod
    def load(cls, path: str | Path) -> "Register":
        data = json.loads(Path(path).read_text())
        risks = [Risk(**r) for r in data["risks"]]
        return cls(risks, appetite=data.get("risk_appetite", 10.0))

    def validate(self) -> list[str]:
        errs, seen = [], set()
        for r in self.risks:
            if r.id in seen:
                errs.append(f"{r.id}: duplicate ID")
            seen.add(r.id)
            errs.extend(r.validate())
        return errs

    def top(self, n: int = 5) -> list[Risk]:
        return sorted(self.risks, key=lambda r: (r.residual, r.residual_ale), reverse=True)[:n]

    def appetite_breaches(self) -> list[Risk]:
        """Residual risk above appetite that is not being actively mitigated."""
        return [r for r in self.risks if r.residual > self.appetite and r.treatment != "mitigate"]

    def overdue(self) -> list[Risk]:
        return [r for r in self.risks if r.overdue()]

    def by(self, attr: str) -> dict[str, list[Risk]]:
        groups: dict[str, list[Risk]] = defaultdict(list)
        for r in self.risks:
            groups[getattr(r, attr)].append(r)
        return dict(groups)

    def totals(self) -> dict[str, float]:
        inh = sum(r.ale for r in self.risks)
        res = sum(r.residual_ale for r in self.risks)
        return {"inherent_ale": inh, "residual_ale": res,
                "risk_reduction_pct": 100 * (1 - res / inh) if inh else 0.0}

    def heatmap(self) -> list[list[list[str]]]:
        """5x5 grid, rows = impact 5..1, cols = likelihood 1..5. Cells hold risk IDs."""
        grid = [[[] for _ in range(5)] for _ in range(5)]
        for r in self.risks:
            grid[5 - r.impact][r.likelihood - 1].append(r.id)
        return grid

    def rating_counts(self) -> dict[str, int]:
        counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
        for r in self.risks:
            counts[rating(r.residual)] += 1
        return counts
