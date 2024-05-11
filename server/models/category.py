from datetime import datetime
from models import common
from pydantic import BaseModel, Field
from uuid import UUID


class CategoryBase(BaseModel):
    """
    Category base model

    Attributes:
    - name: str
    - icon: emoji
    """

    name: str = Field(
        min_length=2,
        max_length=16,
        description="Category name must be 2-16 characters long.",
    )
    icon: str = Field(
        default="📦",
        pattern=r"[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U00002600-\U000027BF\U0001f300-\U0001f64F\U0001f680-\U0001f6C0\U0001f6c0-\U0001f6ff]",
        description="Invalid emoji icon.",
    )


class CategoryIn(CategoryBase):
    """
    Category input model

    Attributes:
    - name: str
    - icon: emoji
    """

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Food",
                    "icon": "🍔",
                }
            ]
        },
    }


class CategoryOut(CategoryBase):
    """
    Category output model

    Attributes:
    - uuid: UUID
    - name: str
    - icon: emoji
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
                    "name": "Food",
                    "icon": "🍔",
                    "status": "active",
                    "created_at": "2021-10-01T00:00:00Z",
                    "updated_at": "2021-10-01T00:00:00Z",
                }
            ]
        },
    }
