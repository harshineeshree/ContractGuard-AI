from .document_reader import read_document
from .metadata_extractor import extract_contract_metadata
from .report_generator import generate_contract_report
from .database import save_contract, save_contract_risks


def analyze_contract_file(filename: str) -> str:
    """
    Complete ContractGuard analysis pipeline.

    Flow:
    Contract
        ↓
    Read Document
        ↓
    Extract Metadata
        ↓
    Detect Risks
        ↓
    Save Contract to Supabase
        ↓
    Save Risks to Supabase
        ↓
    Generate Report
    """

    contract_text = read_document(filename)

    if (
        contract_text.startswith("Contract file")
        or contract_text.startswith("Unsupported file type")
        or contract_text.startswith("Error reading")
    ):
        return contract_text

    # Extract contract information and risks
    metadata = extract_contract_metadata(
        filename,
        contract_text
    )

    # Save contract information
    saved_contract = save_contract(metadata)

    if not saved_contract:
        return "Failed to save contract to Supabase."

    # Get the generated contract ID
    contract_id = saved_contract[0]["id"]

    # Save detected risks
    save_contract_risks(
        contract_id,
        metadata.risks
    )

    # Generate final report
    report = generate_contract_report(metadata)

    return report