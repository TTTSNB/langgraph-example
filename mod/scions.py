from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI

import routes as route
import prompts as prompt

# import tools as tool


class DispatcherScion:

    def __init__(self):
        llm = ChatOpenAI(model="gpt-4-turbo")
        toolbox = Toolbox()
        primary_tools = toolbox.get_dispatcher_tools()
        selected_tools = primary_tools
        agent_prompt = prompt.dispatcher_scion_prompt
        self.assistant_runnable = agent_prompt | llm.bind_tools(selected_tools)

    def __call__(self, state: StateGraph):
        while True:
            

            result = self.assistant_runnable.invoke(state)
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)  # noqa
                and not result.content[0].get("text")  # noqa
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break

class InterviewScion:
    def __init__(self, llm, selected_tools, agent_prompt):
        self.assistant_runnable = agent_prompt | llm.bind_tools(selected_tools)

    def __call__(self, state: StateGraph):
        while True:
            result = self.assistant_runnable.invoke(state)
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)  # noqa
                and not result.content[0].get("text")  # noqa
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}


class DispatcherScion(InterviewScion):
    def __init__(self):
        llm = ChatOpenAI(model="gpt-4-turbo")
        toolbox = Toolbox()
        primary_tools = toolbox.get_dispatcher_tools()
        selected_tools = primary_tools
        agent_prompt = prompt.dispatcher_scion_prompt
        super().__init__(
            llm=llm, selected_tools=selected_tools, agent_prompt=agent_prompt
        )


class IntroductionScion(InterviewScion):
    def __init__(self):
        llm = ChatOpenAI(model="gpt-4-turbo")
        toolbox = Toolbox()
        primary_tools = toolbox.get_introduction_tools()
        selected_tools = primary_tools
        agent_prompt = prompt.introduction_scion_prompt
        super().__init__(
            llm=llm, selected_tools=selected_tools, agent_prompt=agent_prompt
        )


class ContactExtractionScion(InterviewScion):
    def __init__(self):
        llm = ChatOpenAI(model="gpt-4-turbo")
        toolbox = Toolbox()
        primary_tools = toolbox.get_contact_extraction_tools()
        selected_tools = primary_tools
        agent_prompt = prompt.contact_extraction_scion_prompt
        super().__init__(
            llm=llm, selected_tools=selected_tools, agent_prompt=agent_prompt
        )


class EquipmentIdentificationScion(InterviewScion):
    def __init__(self):
        llm = ChatOpenAI(model="gpt-4-turbo")
        toolbox = Toolbox()
        primary_tools = toolbox.get_equipment_identification_tools()
        selected_tools = primary_tools
        agent_prompt = prompt.equipment_identification_scion_prompt
        super().__init__(
            llm=llm, selected_tools=selected_tools, agent_prompt=agent_prompt
        )


class Toolbox:
    def __init__(self):

        self.dispatcher_tools = [
            route.ToIntroductionScion,
            route.ToContactExtractionScion,
            route.ToEquipmentIdentificationScion,
            route.CompleteOrEscalate,
        ]

        self.introduction_tools = [
            route.CompleteOrEscalate,
        ]

        self.contact_extraction_tools = [
            route.CompleteOrEscalate,
        ]

        self.equipment_identification_tools = [
            route.CompleteOrEscalate,
        ]

    def get_dispatcher_tools(self):
        return self.dispatcher_tools

    def get_introduction_tools(self):
        return self.introduction_tools

    def get_contact_extraction_tools(self):
        return self.contact_extraction_tools

    def get_equipment_identification_tools(self):
        return self.equipment_identification_tools
