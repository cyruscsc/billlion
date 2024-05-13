from datetime import datetime
from models import common
from pydantic import BaseModel, Field
from uuid import UUID


class UserBase(BaseModel):
    """
    User base model

    Attributes:
    - username: str
    """

    username: str = Field(
        min_length=4,
        max_length=16,
        pattern=r"^[a-z0-9_]+$",
        description="Username must be 4-16 characters long and only contain lowercase letters, numbers and underscores.",
    )


class UserAuth(UserBase):
    """
    User authentication model

    Attributes:
    - username: str
    - password: str
    """

    password: str = Field(
        min_length=8,
        pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,}$",
        description="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number and one special character.",
    )

    model_config = {
        "regex_engine": "python-re"  # Workaround for pydantic v2 Rust regex crate issue
    }


class UserInfo(UserBase):
    """
    User info model

    Attributes:
    - username: str
    - email: str
    - display_name: str
    """

    email: str = Field(
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        description="Invalid email address.",
    )
    display_name: str = Field(
        default=None,
        min_length=2,
        max_length=16,
        description="Display name must be 2-16 characters long.",
    )


class UserInWithInfo(UserAuth, UserInfo):
    """
    User request body model with user info

    Attributes:
    - username: str
    - email: str
    - display_name: str
    - password: str
    """

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "johndoe",
                    "email": "jdoe@example.com",
                    "display_name": "John Doe",
                    "password": "Password123!",
                }
            ]
        },
    }


class UserInWithoutInfo(UserAuth):
    """
    User request body model without user info

    Attributes:
    - username: str
    - password: str
    """

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "johndoe",
                    "password": "Password123!",
                }
            ]
        },
    }


class UserOut(UserInfo):
    """
    User response body model

    Attributes:
    - uuid: UUID
    - username: str
    - email: str
    - display_name: str
    - status: "active" | "inactive"
    - created_at: datetime
    - updated_at: datetime
    """

    uuid: UUID
    status: common.Status
    created_at: datetime
    updated_at: datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "uuid": "550e8400-e29b-41d4-a716-446655440000",
                    "username": "johndoe",
                    "email": "jdoe@example.com",
                    "display_name": "John Doe",
                    "status": "active",
                    "created_at": "2021-10-01T00:00:00Z",
                    "updated_at": "2021-10-01T00:00:00Z",
                }
            ]
        },
    }
