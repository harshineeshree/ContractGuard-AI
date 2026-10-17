from .document_reader import read_document
from .metadata_extractor import extract_contract_metadata
from .ai_analysis_model import AIAnalysis


def prepare_ai_analysis(filename: str) -> AIAnalysis:
    """
    Reads a contract and prepares its information
    for AI-powered analysis.
    """

    # Step 1: Read the contract
    contract_text = read_document(filename)

    # Check for reading errors
    if (
        contract_text.startswith("Contract file")
        or contract_text.startswith("Unsupported file type")
        or contract_text.startswith("Error reading")
    ):
        return AIAnalysis(
            contract_summary=contract_text,
            confidence="Not assessed"
        )

    # Step 2: Extract basic metadata
    metadata = extract_contract_metadata(
        filename,
        contract_text
    )

    # Step 3: Prepare a structured summary
    extracted_information = f"""
Contract Type: {metadata.contract_type or "Not specified"}

Parties: {metadata.parties or "Not specified"}

Effective Date: {metadata.effective_date or "Not specified"}

Expiration Date: {metadata.expiration_date or "Not specified"}

Contract Duration: {metadata.contract_duration or "Not specified"}

Renewal Terms: {metadata.renewal_terms or "Not specified"}

Renewal Notice Period: {metadata.renewal_notice_period or "Not specified"}

Termination Notice Period: {metadata.termination_notice_period or "Not specified"}

Payment: {metadata.payment_amount or "Not specified"}

Payment Frequency: {metadata.payment_frequency or "Not specified"}

Confidentiality: {metadata.confidentiality or "Not specified"}

Governing Law: {metadata.governing_law or "Not specified"}

Dispute Resolution: {metadata.dispute_resolution or "Not specified"}

Scope of Work: {metadata.scope_of_work or "Not specified"}
""".strip()

    # Step 4: Create AI analysis object
    return AIAnalysis(
        contract_summary=(
            f"Contract '{filename}' is ready for AI analysis."
        ),
        extracted_information=extracted_information,
        risks=[],
        missing_clauses=[],
        important_obligations=[],
        confidence="Not assessed",
    )