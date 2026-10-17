import os

from dotenv import load_dotenv
from supabase import create_client, Client


load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "SUPABASE_URL and SUPABASE_KEY must be set in .env"
    )


supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


def test_connection():
    """
    Tests the connection to Supabase.
    """

    response = (
        supabase
        .table("contracts")
        .select("id")
        .limit(1)
        .execute()
    )

    return response.data


def save_contract(metadata):
    """
    Saves analyzed contract metadata into Supabase.
    """

    contract_data = {
        "filename": metadata.filename,
        "contract_type": metadata.contract_type,
        "parties": metadata.parties,
        "effective_date": metadata.effective_date,
        "expiration_date": metadata.expiration_date,
        "contract_duration": metadata.contract_duration,
        "renewal_terms": metadata.renewal_terms,
        "renewal_notice_period": metadata.renewal_notice_period,
        "renewal_deadline": metadata.renewal_deadline,
        "renewal_deadline_status": metadata.renewal_deadline_status,
        "termination_notice_period": metadata.termination_notice_period,
        "payment_amount": metadata.payment_amount,
        "payment_frequency": metadata.payment_frequency,
        "confidentiality": metadata.confidentiality,
        "governing_law": metadata.governing_law,
        "dispute_resolution": metadata.dispute_resolution,
        "scope_of_work": metadata.scope_of_work,
        "important_obligations": metadata.important_obligations,
        "risk_level": metadata.risk_level,
        "status": metadata.status,
    }

    response = (
        supabase
        .table("contracts")
        .insert(contract_data)
        .execute()
    )

    return response.data


def save_contract_risks(contract_id, risks):
    """
    Saves detected contract risks into Supabase.
    """

    if not risks:
        return []

    risk_data = []

    for risk in risks:
        risk_data.append({
            "contract_id": contract_id,
            "risk": risk.risk,
            "evidence": risk.evidence,
            "explanation": risk.explanation,
            "severity": risk.severity,
        })

    response = (
        supabase
        .table("contract_risks")
        .insert(risk_data)
        .execute()
    )

    return response.data