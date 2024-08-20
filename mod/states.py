from typing import TypedDict, Annotated, Sequence, Literal, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from datetime import date
from pydantic import BaseModel
from pydantic.fields import Field


def update_dialog_stack(left: list[str], right: Optional[str]) -> list[str]:
    """Push or pop the state."""
    if right is None:
        return left
    if right == "pop":
        return left[:-1]
    return left + [right]


class InterviewTemplate(BaseModel):
    pass


class InterviewSubject(InterviewTemplate):
    first_name: str = Field(
        ...,
        description="The first name of the interview subject",
        examples=["John", "Jane", "Alice"],
    )
    last_name: str = Field(
        ...,
        description="The last name of the interview subject",
        examples=["Doe", "Smith", "Johnson"],
    )
    full_name: str = Field(
        ...,
        description="The full name of the interview subject",
        examples=["John Doe", "Jane Smith", "Alice Johnson"],
    )
    supervisor_first_name: str = Field(
        ...,
        description="The first name of the supervisor",
        examples=["John", "Jane", "Alice"],
    )
    supervisor_last_name: str = Field(
        ...,
        description="The last name of the supervisor",
        examples=["Doe", "Smith", "Johnson"],
    )
    supervisor_full_name: str = Field(
        ...,
        description="The full name of the supervisor",
        examples=["John Doe", "Jane Smith", "Alice Johnson"],
    )
    last_day_of_work: date = Field(
        ...,
        description="The last day of work for the interview subject",
    )
    department: str = Field(
        ...,
        description="The department the interview subject worked in",
    )
    role: str = Field(
        ...,
        description="The role of the interview subject",
    )


class ExitInterviewContact(InterviewTemplate):
    first_name: str = Field(
        ...,
        description="The first name of the subject's contact",
        examples=["John", "Jane", "Alice"],
    )
    last_name: str = Field(
        ...,
        description="The last name of the subject's contact",
        examples=["Doe", "Smith", "Johnson"],
    )
    full_name: str = Field(
        ...,
        description="The full name of the subject",
        examples=["John Doe", "Jane Smith", "Alice Johnson"],
    )
    company: str = Field(
        ...,
        description="The company the subject's contact works for",
        examples=["Google", "Facebook", "Amazon"],
    )
    phone: str = Field(
        ...,
        description="The phone number of the subject's contact",
        examples=["+1234567890", "+0987654321"],
    )
    email: str = Field(
        ...,
        description="The email of the subject's contact",
        examples=["johndo@email.com", "janesmith@email.com"],
    )
    reason: str = Field(
        ...,
        description="The reason for the contact",
        examples=["Reference", "Recommendation", "Supplier of goods"],
    )


class IntroductionState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], 'add_messages']
    interview_subject: InterviewSubject
    introductions_complete: bool = False


class ContactState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    subject_contact: Annotated[ExitInterviewContact, add_messages]
    contacts_captured: bool = False


class InterviewState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], 'add_messages']
    interview_type: str
    interview_stage: Annotated[
        list[
            Literal[
                "dispatcher_workflow",
                "introduction_workflow",
                "contact_workflow",
                ""
            ]
        ],
        update_dialog_stack,
    ]
    interview_subject: InterviewSubject
    subject_contact: Annotated[ExitInterviewContact, add_messages]
    introductions_complete: bool
    contacts_captured: bool
