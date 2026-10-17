from dataclasses import dataclass

from .ai_analysis_model import AIAnalysis


@dataclass
class AIAgentTasks:
    """
    Stores the tasks prepared for the AI agents.
    """

    intelligence_prompt: str

    risk_prompt: str


def build_intelligence_prompt(
    filename: str,
    contract_text: str
) -> str:
    """
    Builds the task for the Contract Intelligence Agent.
    """

    return f"""
Analyze the following contract.

Filename:
{filename}

Contract:
{contract_text}

Extract:

1. Contract Type
2. Parties
3. Effective Date
4. Expiration Date
5. Contract Duration
6. Renewal Terms
7. Renewal Notice Period
8. Termination Notice Period
9. Payment Amount
10. Payment Frequency
11. Confidentiality Requirements
12. Governing Law
13. Dispute Resolution
14. Scope of Work
15. Important Obligations

Rules:

- Use only information present in the contract.
- Do not invent missing information.
- Write "Not specified" when information is missing.
- Clearly separate facts from interpretation.
"""


def build_risk_prompt(
    filename: str,
    contract_text: str
) -> str:
    """
    Builds the task for the Contract Risk Agent.
    """

    return f"""
Analyze the following contract for potential risks.

Filename:
{filename}

Contract:
{contract_text}

Look for:

1. Automatic renewal
2. Renewal deadlines
3. Termination conditions
4. Payment risks
5. Missing scope of work
6. Missing SLA
7. Confidentiality issues
8. Missing dispute resolution
9. Missing governing law
10. Ambiguous clauses

For every risk provide:

- Risk
- Evidence
- Explanation
- Severity

Severity must be:

Low
Medium
High

Rules:

- Do not invent information.
- Base findings on the contract.
- Do not provide legal advice.
"""


def prepare_ai_agent_tasks(
    filename: str,
    contract_text: str
) -> AIAgentTasks:
    """
    Creates tasks for both AI agents.
    """

    intelligence_prompt = build_intelligence_prompt(
        filename,
        contract_text
    )

    risk_prompt = build_risk_prompt(
        filename,
        contract_text
    )

    return AIAgentTasks(
        intelligence_prompt=intelligence_prompt,
        risk_prompt=risk_prompt,
    )


def create_ai_analysis() -> AIAnalysis:
    """
    Creates an empty AI analysis result.

    Gemini execution will be connected later.
    """

    return AIAnalysis(
        contract_summary=None,
        extracted_information=None,
        risks=[],
        missing_clauses=[],
        important_obligations=[],
        confidence="Not assessed",
    )