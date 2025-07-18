from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from deep_research_agent.api.conversation_manager import conversation_manager
from deep_research_agent.common.schemas import AwaitingUserInputError
from deep_research_agent.core.workflow import DEFAULT_WORKFLOW, get_workflow_metadata

app = FastAPI(
    title="Deep Research Agent API",
    description="API for orchestrating a multi-agent deep research workflow.",
    version="0.1.0",
    root_path="/deepresearch-api-stage",
)


class StartRequest(BaseModel):
    company_name: str
    company_url: str
    action: str
    uploaded_files: list[str] = []  # S3 URLs or local file paths


class ConversationResponse(BaseModel):
    response: str


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.get("/workflow/metadata")
async def get_default_workflow_metadata():
    """
    Get metadata for the default workflow steps.
    This provides information about each step including descriptions,
    estimated durations, and expected outputs.
    """
    return {
        "workflow_metadata": get_workflow_metadata(),
        "total_steps": len(DEFAULT_WORKFLOW),
        "workflow_description": "Deep Research Agent multi-step workflow for comprehensive company analysis and use case generation",
    }


@app.get("/research/{conversation_id}/status")
async def get_workflow_status(conversation_id: str):
    """
    Get the current workflow status and progress for a conversation.
    Returns detailed information about the workflow execution including:
    - Current step and progress percentage
    - Step history with timing information
    - Workflow context summary
    - Current agent being executed
    """
    orchestrator = conversation_manager.get_conversation(conversation_id)
    if not orchestrator:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return {"conversation_id": conversation_id, "workflow_status": orchestrator.get_workflow_status()}


@app.get("/research/{conversation_id}/context")
async def get_workflow_context(conversation_id: str, include_full_context: bool = False):
    """
    Get the workflow context for a conversation.

    Args:
        conversation_id: The conversation ID
        include_full_context: If True, returns the full workflow_context.
                            If False, returns only a summary for performance.
    """
    orchestrator = conversation_manager.get_conversation(conversation_id)
    if not orchestrator:
        raise HTTPException(status_code=404, detail="Conversation not found")

    if include_full_context:
        return {
            "conversation_id": conversation_id,
            "workflow_context": orchestrator.workflow_context,
            "context_keys": list(orchestrator.workflow_context.keys()),
        }
    else:
        return {
            "conversation_id": conversation_id,
            "context_summary": orchestrator._get_context_summary(),
            "context_keys": list(orchestrator.workflow_context.keys()),
            "context_size": len(orchestrator.workflow_context),
        }


@app.get("/conversations")
async def list_conversations():
    """
    List all active conversations and their current status.
    """
    conversations = []
    for conv_id in conversation_manager.conversations:
        orchestrator = conversation_manager.get_conversation(conv_id)
        if orchestrator:
            status = orchestrator.get_workflow_status()
            conversations.append(
                {
                    "conversation_id": conv_id,
                    "status": status["status"],
                    "progress_percentage": status["progress_percentage"],
                    "current_agent": status["current_agent"],
                    "started_at": status["started_at"],
                    "last_updated": status["last_updated"],
                }
            )

    return {"conversations": conversations}


@app.post("/research")
async def start_research(request: StartRequest):
    """
    Starts a new research conversation and returns the first set of questions.
    """
    if request.action != "start":
        raise HTTPException(status_code=400, detail=f"Invalid action: {request.action}")

    initial_prompt = f"Analyze the company {request.company_name} which can be found at {request.company_url}."

    conversation_id = conversation_manager.create_conversation()
    orchestrator = conversation_manager.get_conversation(conversation_id)
    if not orchestrator:
        raise HTTPException(status_code=500, detail="Failed to create conversation")

    # Add uploaded files to the workflow context if any are provided
    if request.uploaded_files:
        orchestrator.workflow_context["uploaded_files"] = request.uploaded_files

    try:
        result = await orchestrator.start_workflow(initial_prompt)
        # This path should not be hit if ClarifierAgent is first
        return {"status": "completed", "conversation_id": conversation_id, "result": result}
    except AwaitingUserInputError as e:
        # Update status to awaiting_input
        orchestrator._update_status("awaiting_input")
        return {"status": "awaiting_input", "conversation_id": conversation_id, "questions": e.questions}


@app.post("/research/{conversation_id}/respond")
async def respond(conversation_id: str, response: ConversationResponse):
    """
    Continues a conversation with a user's response.
    """
    orchestrator = conversation_manager.get_conversation(conversation_id)
    if not orchestrator:
        raise HTTPException(status_code=404, detail="Conversation not found")

    try:
        result = await orchestrator.continue_workflow(response.response)
        if result.get("status") == "completed":
            conversation_manager.end_conversation(conversation_id)
        return {"status": "use_cases_generated", "result": result}
    except AwaitingUserInputError as e:
        # Update status to awaiting_input
        orchestrator._update_status("awaiting_input")
        return {"status": "awaiting_input", "questions": e.questions}
