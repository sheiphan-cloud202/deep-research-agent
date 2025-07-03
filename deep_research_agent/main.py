from deep_research_agent.core.orchestrator import OrchestratorAgent
from deep_research_agent.utils.logger import logger


def main():
    """
    Main function to run the deep research agent workflow with interactive conversation.
    """
    logger.info("🤖 Welcome to the Deep Research Agent!")
    logger.info("I'll help you develop and refine your idea through conversation.")
    logger.info("When you're ready to start the research process, just say 'start the agent', 'yes', or 'run'.\n")

    # Get initial prompt
    initial_prompt = input("Please describe your initial idea or project: ")
    if not initial_prompt.strip():
        logger.warning("Please provide an initial idea to get started.")
        return

    # Initialize orchestrator and start the workflow
    conversation_history = [initial_prompt]
    orchestrator = OrchestratorAgent()

    logger.info("\n🚀 Starting the deep research agent workflow...\n")
    orchestrator.run_workflow_from_conversation(conversation_history)

    logger.info("\n--- END OF WORKFLOW ---")
    logger.info("✅ Your comprehensive research report is ready!")
    # In a real application, the final_report would be saved to a file or displayed in a UI.


if __name__ == "__main__":
    main()
