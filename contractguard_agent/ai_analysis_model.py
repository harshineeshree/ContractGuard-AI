from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class RiskFinding:
    """
    Represents a potential contractual risk.
    """

    risk: str

    evidence: str

    explanation: str

    severity: str


@dataclass
class AIAnalysis:
    """
    Stores the result of AI-powered contract analysis.
    """

    contract_summary: Optional[str] = None

    extracted_information: Optional[str] = None

    risks: List[RiskFinding] = field(default_factory=list)

    missing_clauses: List[str] = field(default_factory=list)

    important_obligations: List[str] = field(default_factory=list)

    confidence: Optional[str] = None
