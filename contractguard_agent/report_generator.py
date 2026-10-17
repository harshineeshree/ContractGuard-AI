from .contract_model import ContractMetadata


def generate_contract_report(
    metadata: ContractMetadata
) -> str:
    """
    Generates a complete human-readable ContractGuard report.
    """

    # ----------------------------------------
    # BUILD RISK REPORT
    # ----------------------------------------

    risk_section = ""

    if metadata.risks:

        for index, risk in enumerate(
            metadata.risks,
            start=1
        ):
            risk_section += f"""
Risk {index}:
----------------------------------------
Risk:
{risk.risk}

Severity:
{risk.severity}

Evidence:
{risk.evidence}

Explanation:
{risk.explanation}

"""

    else:

        risk_section = """
No contractual risks were detected.
"""

    # ----------------------------------------
    # FINAL REPORT
    # ----------------------------------------

    report = f"""
CONTRACTGUARD AI
========================================

CONTRACT INFORMATION
----------------------------------------

Filename:
{metadata.filename}

Contract Type:
{metadata.contract_type}

Parties:
{metadata.parties or "Not specified"}

Effective Date:
{metadata.effective_date or "Not specified"}

Expiration Date:
{metadata.expiration_date or "Not specified"}

Contract Duration:
{metadata.contract_duration or "Not specified"}

Renewal Terms:
{metadata.renewal_terms or "Not specified"}

Renewal Notice Period:
{metadata.renewal_notice_period or "Not specified"}

Renewal Deadline:
{metadata.renewal_deadline or "Not specified"}

Renewal Deadline Status:
{metadata.renewal_deadline_status or "Not assessed"}

Termination Notice Period:
{metadata.termination_notice_period or "Not specified"}

Payment:
{metadata.payment_amount or "Not specified"}

Payment Frequency:
{metadata.payment_frequency or "Not specified"}

Confidentiality:
{metadata.confidentiality or "Not specified"}

Governing Law:
{metadata.governing_law or "Not specified"}

Dispute Resolution:
{metadata.dispute_resolution or "Not specified"}

Scope of Work:
{metadata.scope_of_work or "Not specified"}

Important Obligations:
{metadata.important_obligations or "Not specified"}

----------------------------------------
RISK INFORMATION
----------------------------------------

Overall Risk Level:
{metadata.risk_level or "Not assessed"}

Contract Status:
{metadata.status or "Unknown"}

Detected Risks:
{risk_section}
========================================
"""

    return report.strip()