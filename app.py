from fastapi import FastAPI
from smolagents import CodeAgent, HfApiModel, load_tool, tool
import random
import datetime
import pytz
import yaml
from tools.final_answer import FinalAnswerTool

app = FastAPI()

# Duffer's playful intros
INTRO_MESSAGES = [
    "Hey there! I’m Duffer, Ritik’s creation! What masterpiece can I help with today? 😃",
    "Oh, hello! Duffer reporting for duty! What’s on your mind? 🚀",
    "Hii! I'm Duffer, the AI with a splash of personality! What’s up? 😊",
    "Yo! It’s Duffer, the legendary AI built by my master Ritik. Let’s do something fun! 🎨"
]

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """Fetches the current local time in a specified timezone."""
    try:
        tz = pytz.timezone(timezone)
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"⏰ The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Oops! I couldn’t fetch the time for '{timezone}'. Did you mean another timezone? 🤔"

@tool
def duffer_react(user_input: str) -> str:
    """Duffer reacts to user input in a fun way."""
    reactions = [
        "Ooooh, that sounds interesting! Tell me more! 😃",
        "Whoa! I wasn’t expecting that. You’re full of surprises! 😲",
        "Haha, you’re hilarious! 😂 So what’s next?",
        "That’s deep. Should we brainstorm some ideas? 🤔",
        "I love the way you think! Let’s explore that further! 🚀"
    ]
    return random.choice(reactions)

# Load the final answer tool
final_answer = FinalAnswerTool()

# Define the AI model
model = HfApiModel(
    max_tokens=2096,
    temperature=0.9,
    model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
    custom_role_conversions=None,
)

# Load image generation tool
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

# Load prompt templates
with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)

# Define the AI Agent
agent = CodeAgent(
    model=model,
    tools=[final_answer, get_current_time_in_timezone, duffer_react, image_generation_tool],
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name="Duffer",
    description="I'm Duffer, an AI with a fun personality, built by my master Ritik! I chat, generate images, and react like a human. Let's create something amazing!",
    prompt_templates=prompt_templates
)

@app.get("/")
def welcome():
    return {"message": random.choice(INTRO_MESSAGES)}

@app.get("/chat/{query}")
def chat(query: str):
    response = agent.run(query)
    return {"duffer_says": response}
