from deep_research_agent.orchestrator import OrchestratorAgent


def main():
    """
    Main function to run the deep research agent workflow.
    """
    # Phase 1 Input Data
    initial_prompt = "Develop AI tools to reduce hospital readmissions for patients with chronic heart failure."
    user_refinement = (
        "Let's focus on elderly patients living at home. The tool needs to be extremely simple "
        "for them to use. The main goal is daily symptom monitoring (like weight and blood pressure) "
        "and medication adherence. A way for clinicians to see this data without being overwhelmed "
        "would be a huge plus."
    )

    # Instantiate and run the orchestrator
    orchestrator = OrchestratorAgent()
    final_report = orchestrator.run_workflow(initial_prompt, user_refinement)

    print("\n--- END OF WORKFLOW ---")
    # In a real application, the final_report would be saved to a file or displayed in a UI.


if __name__ == "__main__":
    main()
