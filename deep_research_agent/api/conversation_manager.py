import uuid

from deep_research_agent.core.orchestrator import OrchestratorAgent


class ConversationManager:
    def __init__(self):
        self.conversations: dict[str, OrchestratorAgent] = {}

    def create_conversation(self) -> str:
        conversation_id = str(uuid.uuid4())
        self.conversations[conversation_id] = OrchestratorAgent()
        return conversation_id

    def get_conversation(self, conversation_id: str) -> OrchestratorAgent | None:
        return self.conversations.get(conversation_id)

    def end_conversation(self, conversation_id: str):
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]


conversation_manager = ConversationManager()
