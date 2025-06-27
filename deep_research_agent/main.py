from deep_research_agent.orchestrator import OrchestratorAgent


def main():
    """
    Main function to run the deep research agent workflow with interactive conversation.
    """
    print("🤖 Welcome to the Deep Research Agent!")
    print("I'll help you develop and refine your idea through conversation.")
    print("When you're ready to start the research process, just say 'start the agent', 'yes', or 'run'.\n")
    
    # Get initial prompt
    initial_prompt = input("Please describe your initial idea or project: ")
    if not initial_prompt.strip():
        print("Please provide an initial idea to get started.")
        return
    
    # Start conversation flow
    conversation_history = [initial_prompt]
    trigger_words = ["start the agent", "yes", "run", "start agent", "begin", "go"]
    
    print(f"\n💭 Great! Let me ask you some clarifying questions to better understand your idea...\n")
    
    # Initialize orchestrator and clarifier
    orchestrator = OrchestratorAgent()
    
    while True:
        # Generate clarifying questions based on current conversation
        clarifying_questions = orchestrator.generate_clarifying_questions(conversation_history)
        print(f"🤔 {clarifying_questions}\n")
        
        # Get user response
        user_response = input("Your response (or say 'start the agent'/'yes'/'run' when ready): ").strip()
        
        if not user_response:
            print("Please provide a response or say when you're ready to start.\n")
            continue
            
        # Check for trigger words
        if any(trigger.lower() in user_response.lower() for trigger in trigger_words):
            print("\n🚀 Starting the deep research agent workflow...\n")
            break
            
        # Add response to conversation history
        conversation_history.append(user_response)
        print()  # Add spacing for readability
    
    # Run the main workflow with conversation history
    final_report = orchestrator.run_workflow_from_conversation(conversation_history)

    print("\n--- END OF WORKFLOW ---")
    print("✅ Your comprehensive research report is ready!")
    # In a real application, the final_report would be saved to a file or displayed in a UI.


if __name__ == "__main__":
    main()
