from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TodoCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Title of the todo",
    )
    description: str = Field(
        default="",
        max_length=2000,
    )


class TodoUpdate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
    )
    description: str = Field(
        default="",
        max_length=2000,
    )
    completed: bool


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)