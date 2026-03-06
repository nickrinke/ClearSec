from pydantic import BaseModel
from typing import List, Optional

class ControlScore(BaseModel):
    control_name: str
    control_category: str
    description: str
    score: float
    max_score: float = 0.0
    score_in_percentage: float
    implementation_status: str

    @property
    def is_failing(self) -> bool:
        return self.score_in_percentage < 100.0

class SecureScoreReport(BaseModel):
    tenant_id: str
    current_score: float
    max_score: float
    active_user_count: int
    controls: List[ControlScore]

    @property
    def failing_controls(self) -> List[ControlScore]:
        return [c for c in self.controls if c.is_failing]

    @classmethod
    def from_graph(cls, data: dict) -> "SecureScoreReport":
        controls = [
            ControlScore(
                control_name=c.get("controlName", ""),
                control_category=c.get("controlCategory", ""),
                description=c.get("description", ""),
                score=c.get("score", 0.0),
                score_in_percentage=c.get("scoreInPercentage", 0.0),
                implementation_status=c.get("implementationStatus", ""),
            )
            for c in data.get("controlScores", [])
        ]
        return cls(
            tenant_id=data.get("azureTenantId", ""),
            current_score=data.get("currentScore", 0.0),
            max_score=data.get("maxScore", 0.0),
            active_user_count=data.get("activeUserCount", 0),
            controls=controls,
        )
