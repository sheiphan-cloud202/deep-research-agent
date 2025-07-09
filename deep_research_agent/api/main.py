from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from deep_research_agent.api.conversation_manager import conversation_manager
from deep_research_agent.common.schemas import AwaitingUserInputError

app = FastAPI(
    title="Deep Research Agent API",
    description="API for orchestrating a multi-agent deep research workflow.",
    version="0.1.0",
)


class StartRequest(BaseModel):
    company_name: str
    company_url: str
    action: str
    uploaded_files: list[str] = []


class ConversationResponse(BaseModel):
    response: str


@app.get("/")
def read_root():
    return {"status": "ok"}


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
    try:
        result = await orchestrator.start_workflow(initial_prompt)
        # This path should not be hit if ClarifierAgent is first
        return {"status": "completed", "conversation_id": conversation_id, "result": result}
    except AwaitingUserInputError as e:
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
        return {"status": "completed", "result": result}
    except AwaitingUserInputError as e:
        return {"status": "awaiting_input", "questions": e.questions}
