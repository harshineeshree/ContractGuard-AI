from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class RiskFinding:
    """
    Represents a detected contract risk.
    """

    risk: str
    evidence: str
    explanation: str
    severity: str


@dataclass
class ContractMetadata:
    filename: str

    contract_type: Optional[str] = None
    parties: Optional[str] = None

    effective_date: Optional[str] = None
    expiration_date: Optional[str] = None
    contract_duration: Optional[str] = None

    renewal_terms: Optional[str] = None
    renewal_notice_period: Optional[str] = None
    renewal_deadline: Optional[str] = None
    renewal_deadline_status: Optional[str] = None

    termination_notice_period: Optional[str] = None

    payment_amount: Optional[str] = None
    payment_frequency: Optional[str] = None

    confidentiality: Optional[str] = None
    governing_law: Optional[str] = None
    dispute_resolution: Optional[str] = None
    scope_of_work: Optional[str] = None
    important_obligations: Optional[str] = None

    risks: List[RiskFinding] = field(default_factory=list)

    risk_level: Optional[str] = None
    status: Optional[str] = None