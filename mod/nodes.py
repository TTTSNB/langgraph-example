from functools import lru_cache

# from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.chains.openai_functions.tagging import create_tagging_chain
from langgraph.prebuilt import ToolNode

from mod import tools as tool
from mod import prompts as prompt
from mod.states import InterviewSubject, InterviewTemplate


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
    model.bind_tools(tool.tavily_tool)
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


def call_dispatcher(state, config):
    messages = state["messages"]
    messages = [{"role": "system", "content": prompt.dispatcher_prompt}] + messages
    model_name = config.get("configurable", {}).get("model_name", "openai")
    model = get_model(model_name)
    model.bind_tools(tool.dispatcher_tools)
    response = model.invoke(messages)
    return {"messages": [response]}


def get_subject(state):
    if "interview_subject" not in state:
        interview_subject = InterviewSubject(
            first_name="",
            last_name="",
            full_name="",
            supervisor_first_name="",
            supervisor_last_name="",
            supervisor_full_name="",
            last_day_of_work="",
            department="",
            role="",
        )
        return state["interview_subject":interview_subject]
    else:
        return state["interview_subject"]


def check_what_is_empty(form: InterviewTemplate) -> list:
    return [
        field for field, value in form.model_dump().items() if value in [None, "", 0]
    ]


def add_non_empty_details(
    current_details: InterviewTemplate, additional_details: InterviewTemplate
) -> InterviewTemplate:
    non_empty_details = {k: v for k, v in additional_details.model_dump().items() if v}
    return current_details.model_copy(update=non_empty_details)


def determine_what_to_ask_for(state):
    interview_subject = get_subject(state)
    ask_for = check_what_is_empty(form=interview_subject)
    if ask_for == []:
        state["introductions_complete"] = True
    
    else:
        
    interview_subject = state["interview_subject"]
    model_name = config.get("configurable", {}).get("model_name", "openai")
    model = get_model(model_name)
    chain = create_tagging_chain(schema=interview_subject, llm=model)

    messages = [
        {"role": "system", "content": prompt.personal_details_prompt}
    ] + messages
    model_name = config.get("configurable", {}).get("model_name", "openai")
    model = get_model(model_name)
    model.bind_tools(tool.personal_details_tools)
    response = model.invoke(messages)
    return {{**state, "messages": [response]}}
