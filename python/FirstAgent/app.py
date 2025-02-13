from smolagents import CodeAgent, DuckDuckGoSearchTool, OpenAIServerModel, load_tool, tool
import datetime
import requests
import pytz
import yaml
from dotenv import load_dotenv
import os
from tools.final_answer import FinalAnswerTool
from Gradio_UI import GradioUI
import random

load_dotenv()


# Access variables
@tool
def my_cutom_tool(arg1: str, arg2: int) -> str:  # it's import to specify the return type
    # Keep this format for the description / args / args description but feel free to modify the tool
    """A tool that does nothing yet
    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return "What magic will you build ?"


@tool
def flip_a_coin() -> str:
    """A tool that flips a coin for you. Returns either "Head" or "Tails".
    Args:
        None
    """
    return random.choice(["Head", "Tails"])


@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


final_answer = FinalAnswerTool()
model = OpenAIServerModel(
    max_tokens=2096,
    temperature=0.5,
    model_id="gpt-4o-mini",
    api_key=os.getenv("OPENAI_KEY"),
)

# Import tool from Hub
image_generation_tool = load_tool(
    "agents-course/text-to-image", trust_remote_code=True)

with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)

agent = CodeAgent(
    model=model,
    tools=[final_answer, get_current_time_in_timezone, flip_a_coin],  # add your tools here (don't remove final answer)
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates
)


GradioUI(agent).launch()
