from nemoguardrails import RailsConfig
from nemoguardrails.integrations.langchain.runnable_rails import (
    RunnableRails
)
from dotenv import load_dotenv
import os

load_dotenv()

CONFIG_PATH = "backend/guardrails"

config = RailsConfig.from_path(CONFIG_PATH)

guardrails = RunnableRails(
    config=config,
    passthrough=True,
    verbose=True
)