"""Risk model: qualitative (5x5) and quantitative (ALE) scoring."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date

TREATMENTS = {"mitigate", "accept", "transfer", "avoid"}
CSF_FUNCTIONS = {"govern", "identify", "protect", "detect", "respond", "recover"}


def rating(score: float) -> str:
    """Map a 1-25 score to a qualitative band."""
    if score >= 15:
        return "Critical"
    if score >= 10:
        return "High"
    if score >= 5:
        return "Medium"
    return "Low"


@dataclass
class Risk:
    id: str
    title: str
    asset: str
    threat: str
    csf_function: str
    cissp_domain: str
    likelihood: int            # 1-5
    impact: int                # 1-5
    control_effectiveness: float  # 0.0-1.0
    asset_value: float         # USD
    exposure_factor: float     # 0.0-1.0 (fraction of value lost per event)
    aro: float                 # annualised rate of occurrence
    owner: str
    treatment: str
    review_date: str           # ISO date

    @property
    def inherent(self) -> int:
        return self.likelihood * self.impact

    @property
    def residual(self) -> float:
        return round(self.inherent * (1 - self.control_effectiveness), 2)

    @property
    def sle(self) -> float:
        """Single Loss Expectancy = AV x EF."""
        return self.asset_value * self.exposure_factor

    @property
    def ale(self) -> float:
        """Annualised Loss Expectancy = SLE x ARO."""
        return self.sle * self.aro

    @property
    def residual_ale(self) -> float:
        return self.ale * (1 - self.control_effectiveness)

    def overdue(self, today: date | None = None) -> bool:
        return date.fromisoformat(self.review_date) < (today or date.today())

    def validate(self) -> list[str]:
        errs = []
        if not (1 <= self.likelihood <= 5 and 1 <= self.impact <= 5):
            errs.append(f"{self.id}: likelihood/impact must be 1-5")
        if not 0 <= self.control_effectiveness <= 1:
            errs.append(f"{self.id}: control_effectiveness must be 0-1")
        if not 0 <= self.exposure_factor <= 1:
            errs.append(f"{self.id}: exposure_factor must be 0-1")
        if self.aro < 0 or self.asset_value < 0:
            errs.append(f"{self.id}: aro and asset_value must be >= 0")
        if self.treatment not in TREATMENTS:
            errs.append(f"{self.id}: treatment must be one of {sorted(TREATMENTS)}")
        if self.csf_function.lower() not in CSF_FUNCTIONS:
            errs.append(f"{self.id}: unknown NIST CSF 2.0 function '{self.csf_function}'")
        try:
            date.fromisoformat(self.review_date)
        except ValueError:
            errs.append(f"{self.id}: review_date must be ISO format (YYYY-MM-DD)")
        return errs
