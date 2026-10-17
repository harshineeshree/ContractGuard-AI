from .ai_agent_service import prepare_ai_agent_tasks


def prepare_contract_analysis(
    filename: str,
    contract_text: str
):
    """
    Prepares the contract analysis tasks
    for the ADK multi-agent workflow.
    """

    tasks = prepare_ai_agent_tasks(
        filename,
        contract_text
    )

    return {
        "filename": filename,
        "intelligence_task": tasks.intelligence_prompt,
        "risk_task": tasks.risk_prompt,
    }