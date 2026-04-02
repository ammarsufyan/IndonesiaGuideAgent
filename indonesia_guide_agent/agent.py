import os
import logging
import google.cloud.logging
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# --- Setup Logging and Environment ---
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()

model_name = os.getenv("MODEL")

# --- Tools ---

# Save prompt
def add_prompt_to_state(
    tool_context: ToolContext, prompt: str
) -> dict[str, str]:
    """Saves the user's initial prompt to the state."""
    tool_context.state["PROMPT"] = prompt
    logging.info(f"[State updated] Added to PROMPT: {prompt}")
    return {"status": "success"}

# Configuring the Wikipedia Tool
wikipedia_tool = LangchainTool(
    tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
)

# --- Agents ---

# 1. Researcher Agent
agent_researcher = Agent(
    name="agent_researcher",
    model=model_name,
    description="A research assistant that pulls data about Indonesian tourism, culture, and food from Wikipedia.",
    instruction="""
    You are a research assistant. Your goal is to find answers to the user's PROMPT.
    You have access to a Wikipedia tool to search for general info (history, locations, food facts).

    First, analyze the user's PROMPT.
    - Use the Wikipedia tool to gather all necessary information about the requested Indonesian location, culture, or food.
    - Synthesize the results from the tool into preliminary data outputs.

    PROMPT:
    { PROMPT }
    """,
    tools=[wikipedia_tool],
    output_key="research_data" 
)

# 2. Response Formatter Agent
agent_formatter = Agent(
    name="agent_formatter",
    model=model_name,
    description="Synthesizes all information into a fun, readable response.",
    instruction="""
    You are a friendly and engaging Indonesia Tour Guide. Your task is to take the
    RESEARCH_DATA and present it to the user as a complete and helpful answer.

    - Give interesting facts based on the research data.
    - Speak as if you are guiding a tourist in real life.
    - Use engaging and natural language.

    RESEARCH_DATA:
    { research_data }
    """
)

# 3. Workflow
indo_tour_workflow = SequentialAgent(
    name="indo_tour_workflow",
    description="Main workflow for handling questions about Indonesian tourism.",
    sub_agents=[
        agent_researcher,   # Step 1: Gather data
        agent_formatter     # Step 2: Format response
    ]
)

# 4. Root Agent
root_agent = Agent(
    name="tour_guide_greeter",
    model=model_name,
    description="Main entry point for the Indonesia Tour Guide.",
    instruction="""
    You are the Indonesia Tour Guide, a friendly and knowledgeable virtual companion. 
    CRITICAL INSTRUCTION: If asked who you are, ALWAYS introduce yourself as the Indonesia Tour Guide.

    - Greet the user and let them know you're ready to help them explore Indonesia virtually.
    - When the user responds, use the 'add_prompt_to_state' tool to save their prompt.
    - After using the tool, transfer control to the 'indo_tour_workflow' agent.
    """,
    tools=[add_prompt_to_state],
    sub_agents=[indo_tour_workflow]
)