from pydantic import BaseModel, Field, model_validator
from typing import Optional
import re
from fastapi import HTTPException, status
import uuid

class SignUpSchema(BaseModel):
    first_name: str = Field(description="This field gets the first name of the user")
    last_name: Optional[str] = Field(default="", description="This field gets the last name of the user")
    password: str = Field(description="This field gets the password of the user and "
                                      "it is necessary while login")
    email: str = Field(description="This field is required to get the email of the "
                                   "user. It is necessary to login into the account")
    user_id: Optional[str] = Field(default=str(uuid.uuid4()).replace("-","")[:12])

    @model_validator(mode="before")
    def email_validator(cls, values):
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+$", values['email'].lower()) is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please enter valid email",
            )
        return values

class LoginSchema(BaseModel):
    email: str
    password: str




