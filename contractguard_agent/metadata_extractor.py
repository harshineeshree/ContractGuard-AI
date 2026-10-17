import re

from .contract_model import ContractMetadata
from .deadline_calculator import calculate_renewal_deadline
from .deadline_status import get_deadline_status
from .risk_engine import (
    analyze_contract_risks,
    calculate_overall_risk,
)


def extract_contract_metadata(
    filename: str,
    contract_text: str
) -> ContractMetadata:
    """
    Extracts contract metadata and performs
    deterministic risk analysis.
    """

    text = contract_text.strip()
    lower_text = text.lower()

    # ----------------------------------------
    # CONTRACT TYPE
    # ----------------------------------------

    contract_type = "Other / Unknown Contract Type"

    if (
        "non-disclosure" in lower_text
        or "confidentiality agreement" in lower_text
    ):
        contract_type = "NDA - Non-Disclosure Agreement"

    elif (
        "service agreement" in lower_text
        or "service provider" in lower_text
    ):
        contract_type = "Service Agreement"

    elif (
        "statement of work" in lower_text
        or "scope of work" in lower_text
    ):
        contract_type = "SOW - Statement of Work"

    elif "purchase agreement" in lower_text:
        contract_type = "Purchase Agreement"

    elif "employment agreement" in lower_text:
        contract_type = "Employment Agreement"

    # ----------------------------------------
    # DATES
    # ----------------------------------------

    effective_date = extract_value(
        text,
        r"Effective Date:\s*(.+)"
    )

    expiration_date = extract_value(
        text,
        r"Expiration Date:\s*(.+)"
    )

    # ----------------------------------------
    # PAYMENT
    # ----------------------------------------

    payment_amount = None
    payment_frequency = None

    payment_match = re.search(
        r"pay.*?(INR\s*[\d,]+)\s*(per\s+\w+)",
        text,
        re.IGNORECASE
    )

    if payment_match:
        payment_amount = payment_match.group(1).strip()
        payment_frequency = payment_match.group(2).strip()

    # ----------------------------------------
    # RENEWAL TERMS
    # ----------------------------------------

    renewal_terms = None

    renewal_match = re.search(
        r"The agreement will\s+"
        r"(automatically renew.*?before expiration\.)",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if renewal_match:
        renewal_terms = clean_text(
            "The agreement will " + renewal_match.group(1)
        )

    # ----------------------------------------
    # RENEWAL NOTICE PERIOD
    # ----------------------------------------

    renewal_notice_period = None

    renewal_notice_match = re.search(
        r"(\d+)\s*days?\s*before\s*expiration",
        text,
        re.IGNORECASE
    )

    if renewal_notice_match:
        renewal_notice_period = (
            renewal_notice_match.group(1) + " days"
        )

    # ----------------------------------------
    # RENEWAL DEADLINE
    # ----------------------------------------

    renewal_deadline = calculate_renewal_deadline(
        expiration_date,
        renewal_notice_period
    )

    # ----------------------------------------
    # DEADLINE STATUS
    # ----------------------------------------

    renewal_deadline_status = get_deadline_status(
        renewal_deadline
    )

    # ----------------------------------------
    # TERMINATION NOTICE PERIOD
    # ----------------------------------------

    termination_notice_period = None

    termination_match = re.search(
        r"terminate.*?(\d+)\s*days?\s*written\s*notice",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if termination_match:
        termination_notice_period = (
            termination_match.group(1) + " days"
        )

    # ----------------------------------------
    # CONFIDENTIALITY
    # ----------------------------------------

    confidentiality = None

    if "confidential" in lower_text:
        confidentiality = "Required"

    # ----------------------------------------
    # PARTIES
    # ----------------------------------------

    parties = None

    parties_match = re.search(
        r"This .*? is between (.*?)\.",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if parties_match:
        parties = clean_text(
            parties_match.group(1)
        )

    # ----------------------------------------
    # CONTRACT DURATION
    # ----------------------------------------

    contract_duration = None

    if effective_date and expiration_date:
        contract_duration = "Approximately 1 year"

    # ----------------------------------------
    # MISSING INFORMATION
    # ----------------------------------------

    governing_law = "Not specified"
    dispute_resolution = "Not specified"
    scope_of_work = "Not specified"
    important_obligations = "Not specified"

    # ----------------------------------------
    # RISK ANALYSIS
    # ----------------------------------------

    risks = analyze_contract_risks(
        contract_text
    )

    risk_level = calculate_overall_risk(
        risks
    )

    # ----------------------------------------
    # CONTRACT STATUS
    # ----------------------------------------

    status = "Active"

    # ----------------------------------------
    # RETURN
    # ----------------------------------------

    return ContractMetadata(
        filename=filename,

        contract_type=contract_type,
        parties=parties,

        effective_date=effective_date,
        expiration_date=expiration_date,
        contract_duration=contract_duration,

        renewal_terms=renewal_terms,
        renewal_notice_period=renewal_notice_period,
        renewal_deadline=renewal_deadline,
        renewal_deadline_status=renewal_deadline_status,

        termination_notice_period=termination_notice_period,

        payment_amount=payment_amount,
        payment_frequency=payment_frequency,

        confidentiality=confidentiality,
        governing_law=governing_law,
        dispute_resolution=dispute_resolution,
        scope_of_work=scope_of_work,
        important_obligations=important_obligations,

        risks=risks,

        risk_level=risk_level,
        status=status,
    )


def extract_value(
    text: str,
    pattern: str
):
    """
    Extracts a value using a regular expression.
    """

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return None


def clean_text(value: str) -> str:
    """
    Cleans unnecessary whitespace.
    """

    return " ".join(value.split())