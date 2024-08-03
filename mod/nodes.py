from functools import lru_cache

# from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langgraph.prebuilt import ToolNode

from mod import tools as tool
from mod import prompts as prompt


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

    model = model.bind_tools(tool.tavily_tool)
    return model


def use_tool(state, config):
    # Define the function to execute tools
    tool_node = ToolNode(tool.tavily_tool)
    return tool_node


# Define the function that calls the model
def call_model(state, config):
    messages = state["messages"]
    messages = [{"role": "system", "content": prompt.system_prompt}] + messages
    model_name = config.get("configurable", {}).get("model_name", "openai")
    model = get_model(model_name)
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}
