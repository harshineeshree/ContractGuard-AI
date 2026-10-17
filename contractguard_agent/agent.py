from google.adk.agents import Agent

from .risk_agent import risk_agent
from .intelligence_agent import intelligence_agent
from .document_reader import read_document


def read_contract(file_name: str) -> str:
    """
    Reads a contract from the local contracts folder.
    """

    return read_document(file_name)


def classify_contract(contract_text: str) -> str:
    """
    Classifies a contract based on its content.
    """

    text = contract_text.lower()

    if (
        "non-disclosure" in text
        or "confidentiality agreement" in text
    ):
        return "NDA - Non-Disclosure Agreement"

    if (
        "service agreement" in text
        or "service provider" in text
    ):
        return "Service Agreement"

    if (
        "statement of work" in text
        or "scope of work" in text
    ):
        return "SOW - Statement of Work"

    if "purchase agreement" in text:
        return "Purchase Agreement"

    if "employment agreement" in text:
        return "Employment Agreement"

    return "Other / Unknown Contract Type"


root_agent = Agent(
    name="contractguard_agent",

    model="gemini-3.6-flash",

    description=(
        "ContractGuard AI is a multi-agent system "
        "for business contract analysis."
    ),

    instruction="""
You are ContractGuard AI, the main contract analysis coordinator.

Your job is to coordinate specialist agents and provide
accurate contract analysis.

==================================================
AVAILABLE SPECIALIST AGENTS
==================================================

1. contract_intelligence_agent

Use this agent when the user asks for:

- Contract information
- Parties
- Dates
- Contract duration
- Renewal terms
- Renewal deadlines
- Termination terms
- Payment information
- Confidentiality
- Governing law
- Dispute resolution
- Scope of work
- Contract obligations

2. risk_agent

Use this agent when the user asks for:

- Contract risks
- Missing clauses
- Weaknesses
- Renewal risks
- Termination risks
- Payment risks
- Compliance concerns
- Ambiguous clauses
- Missing SLA
- Missing governing law
- Missing dispute resolution

==================================================
WORKFLOW
==================================================

When the user provides a contract filename:

STEP 1:
Use read_contract to read the document.

STEP 2:
Identify the contract type.

STEP 3:
If the user asks for contract information,
delegate the task to contract_intelligence_agent.

STEP 4:
If the user asks for risks,
delegate the task to risk_agent.

STEP 5:
If the user asks for a complete analysis,
use both specialist agents and combine their results.

==================================================
IMPORTANT RULES
==================================================

- Never invent contract information.
- If information is missing, say "Not specified".
- Use evidence from the contract.
- Clearly distinguish facts from interpretation.
- Do not provide legal advice.
- Always mention the filename being analyzed.
- Keep the final response clear and structured.
""",

    tools=[
        read_contract,
        classify_contract,
    ],

    sub_agents=[
        intelligence_agent,
        risk_agent,
    ],
)