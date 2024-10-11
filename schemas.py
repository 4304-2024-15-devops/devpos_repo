# Fite to validate the data that is being sent and recieved to the API
import uuid
from typing import Optional
import re

from pydantic import BaseModel, ConfigDict, Field, field_validator

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


class DeleteResponse(BaseModel):
    msg: str = "Todos los datos fueron eliminados"


class CreateBlacklistEmail(BaseModel):
    email: str
    app_uuid: uuid.UUID
    blocked_reason: str = Field(max_length=255)

    model_config = ConfigDict(from_attributes=True)

    # Email validation regex pattern

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if not v:
            raise ValueError("Email is required")
        if not re.match(EMAIL_REGEX, v):
            raise ValueError("Invalid email format")
        return v


class BlacklistCreatedResponse(BaseModel):
    is_blacklisted: bool
    reason: str


class BlacklistSearchResponse(BaseModel):
    is_blacklisted: bool
    blocked_reason: Optional[str]
    model_config = ConfigDict(from_attributes=True)
