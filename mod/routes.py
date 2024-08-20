from langchain_core.pydantic_v1 import BaseModel, Field


class CompleteOrEscalate(BaseModel):
    """A tool to mark the current task as completed and/or to escalate control of the dialog to the main assistant,
    who can re-route the dialog based on the user's needs."""

    cancel: bool = True
    reason: str

    class Config:
        schema_extra = {
            "example": {
                "name": "CompleteOrEscalate",
                "cancel": True,
                "reason": "User changed their mind about the current task.",
            },
            "example 2": {
                "name": "CompleteOrEscalate",
                "cancel": True,
                "reason": "I have fully completed the portion of task relevant to the tools in my possession.",
            },
            "example 3": {
                "name": "CompleteOrEscalate",
                "cancel": False,
                "reason": "I have access to additional information relevant to the users request.",
            },
        }


class ToIntroductionScion(BaseModel):
    """Transfers work to an assistant that specializes in collecting personal information."""

    request: str = Field(
        description="Any necessary followup questions the Introduction Scion should clarify before proceeding."
    )


class ToContactExtractionScion(BaseModel):
    """Transfers work to an assistant that specializes in collecting contact information."""

    request: str = Field(
        description="Any necessary followup questions the Introduction Scion should clarify before proceeding."
    )


class ToEquipmentIdentificationScion(BaseModel):
    """Transfers work to a specialized assistant to handle trip recommendation and other excursion bookings."""

    request: str = Field(
        description="Any additional information or requests from the user regarding portfolio information."
    )
