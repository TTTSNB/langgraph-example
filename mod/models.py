from functools import lru_cache
# from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

from tools import tavily_tool


@lru_cache(maxsize=4)
def get_model(model_name: str):
    if model_name == "openai":
        model = ChatOpenAI(temperature=0, model_name="gpt-4o")
    # elif model_name == "anthropic":
    #     model = ChatAnthropic(temperature=0, model_name="claude-3-sonnet-20240229")
    elif model_name == "ollama":
        model = ChatOllama(model="llama3.1:405b")
    else:
        raise ValueError(f"Unsupported model type: {model_name}")

    model = model.bind_tools(tavily_tool)
    return model
