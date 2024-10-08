from typing import TypedDict, Literal


# Define the config
class GraphConfig(TypedDict):
    model_name: Literal["openai", "ollama"]
    interview_type: Literal["exit", "entry"]
