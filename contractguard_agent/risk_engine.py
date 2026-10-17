from dataclasses import dataclass
from typing import List


@dataclass
class RiskFinding:
    """
    Represents a detected contract risk.
    """

    risk: str
    evidence: str
    explanation: str
    severity: str


def analyze_contract_risks(
    contract_text: str
) -> List[RiskFinding]:
    """
    Performs deterministic risk analysis on a contract.

    This does not use Gemini.
    """

    risks: List[RiskFinding] = []

    text = contract_text.strip()
    lower_text = text.lower()

    # ----------------------------------------
    # AUTOMATIC RENEWAL
    # ----------------------------------------

    if "automatically renew" in lower_text:

        risks.append(
            RiskFinding(
                risk="Automatic Renewal",
                evidence=(
                    "The contract contains an automatic renewal clause."
                ),
                explanation=(
                    "The agreement may renew automatically unless "
                    "the required notice is provided before expiration."
                ),
                severity="Medium",
            )
        )

    # ----------------------------------------
    # GOVERNING LAW
    # ----------------------------------------

    if (
        "governing law" not in lower_text
        and "laws of" not in lower_text
    ):

        risks.append(
            RiskFinding(
                risk="Missing Governing Law",
                evidence="No governing law clause was identified.",
                explanation=(
                    "The contract does not specify which jurisdiction's "
                    "law governs the agreement."
                ),
                severity="Medium",
            )
        )

    # ----------------------------------------
    # DISPUTE RESOLUTION
    # ----------------------------------------

    if not any(
        keyword in lower_text
        for keyword in [
            "dispute resolution",
            "arbitration",
            "mediation",
        ]
    ):

        risks.append(
            RiskFinding(
                risk="Missing Dispute Resolution",
                evidence=(
                    "No dispute resolution, arbitration, "
                    "or mediation clause was identified."
                ),
                explanation=(
                    "The contract does not specify a process "
                    "for resolving disputes."
                ),
                severity="Medium",
            )
        )

    # ----------------------------------------
    # SERVICE LEVEL / SLA
    # ----------------------------------------

    if (
        "service agreement" in lower_text
        or "service provider" in lower_text
    ):

        if not any(
            keyword in lower_text
            for keyword in [
                "service level",
                "sla",
                "service-level agreement",
            ]
        ):

            risks.append(
                RiskFinding(
                    risk="Missing Service Level Agreement",
                    evidence="No SLA or service-level clause was identified.",
                    explanation=(
                        "The service agreement does not define measurable "
                        "service levels or performance commitments."
                    ),
                    severity="Medium",
                )
            )

    # ----------------------------------------
    # SCOPE OF WORK
    # ----------------------------------------

    if (
        "scope of work" not in lower_text
        and "statement of work" not in lower_text
    ):

        risks.append(
            RiskFinding(
                risk="Missing Scope of Work",
                evidence="No explicit scope of work was identified.",
                explanation=(
                    "The contract does not clearly define the services, "
                    "deliverables, or work covered by the agreement."
                ),
                severity="Medium",
            )
        )

    # ----------------------------------------
    # TERMINATION
    # ----------------------------------------

    if "termination" not in lower_text:

        risks.append(
            RiskFinding(
                risk="Missing Termination Clause",
                evidence="No termination clause was identified.",
                explanation=(
                    "The contract does not clearly specify "
                    "termination conditions."
                ),
                severity="High",
            )
        )

    # ----------------------------------------
    # PAYMENT
    # ----------------------------------------

    if not any(
        keyword in lower_text
        for keyword in [
            "payment",
            "pay",
            "invoice",
            "fee",
            "price",
        ]
    ):

        risks.append(
            RiskFinding(
                risk="Missing Payment Terms",
                evidence="No payment-related clause was identified.",
                explanation=(
                    "The contract does not clearly specify "
                    "payment obligations."
                ),
                severity="Medium",
            )
        )

    # ----------------------------------------
    # CONFIDENTIALITY
    # ----------------------------------------

    if "confidential" not in lower_text:

        risks.append(
            RiskFinding(
                risk="Missing Confidentiality Clause",
                evidence="No confidentiality clause was identified.",
                explanation=(
                    "The contract does not appear to define "
                    "confidentiality obligations."
                ),
                severity="Low",
            )
        )

    return risks


def calculate_overall_risk(
    risks: List[RiskFinding]
) -> str:
    """
    Calculates an overall risk level from detected findings.
    """

    if not risks:
        return "Low"

    severities = [
        risk.severity
        for risk in risks
    ]

    if "High" in severities:
        return "High"

    if "Medium" in severities:
        return "Medium"

    return "Low"