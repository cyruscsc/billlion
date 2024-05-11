from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from uuid import UUID


class UserBase(BaseModel):
    """User base model."""

    username: str = Field(
        min_length=4,
        max_length=16,
        pattern=r"^[a-z0-9_]+$",
        description="Username must be 4-16 characters long and only contain lowercase letters, numbers and underscores.",
    )


class UserAuth(UserBase):
    """User authentication model."""

    password: str = Field(
        min_length=8,
        pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,}$",
        description="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number and one special character.",
    )

    model_config = {
        "regex_engine": "python-re"  # Workaround for pydantic v2 Rust regex crate issue
    }


class UserInfo(UserBase):
    """User info model."""

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


class UserRegister(UserAuth, UserInfo):
    """User register model."""

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


class UserLogin(UserAuth):
    """User login model."""

    pass

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
    """User response body model."""

    uuid: UUID
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
                    "created_at": "2021-10-01T00:00:00Z",
                    "updated_at": "2021-10-01T00:00:00Z",
                }
            ]
        },
    }


class SpaceBase(BaseModel):
    """Space base model."""

    name: str = Field(
        min_length=2,
        max_length=16,
        description="Space name must be 2-16 characters long.",
    )
    icon: str | None = None
    members: list[str] | None = None  # List of user UUIDs


class SpaceIn(SpaceBase):
    """Space request body model for space creation and update."""

    pass


class SpaceOut(SpaceBase):
    """Space response body model."""

    uuid: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    """Category base model."""

    name: str = Field(
        min_length=2,
        max_length=16,
        description="Category name must be 2-16 characters long.",
    )
    icon: str | None = None
    space_uuid: UUID


class CategoryIn(CategoryBase):
    """Category request body model for category creation and update."""

    pass


class CategoryOut(CategoryBase):
    """Category response body model."""

    uuid: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Currency(str, Enum):
    """Currency enum class."""

    aud = "AUD"
    cad = "CAD"
    eur = "EUR"
    gbp = "GBP"
    hkd = "HKD"
    jpy = "JPY"
    ntd = "NTD"
    usd = "USD"


class Interval(str, Enum):
    """Interval enum class."""

    day = "day"
    week = "week"
    month = "month"
    year = "year"


class Payer(BaseModel):
    """Payer model."""

    user_uuid: UUID
    amount: float = Field(
        ge=0,
        description="Amount must be a non-negative number.",
    )


class BillBase(BaseModel):
    """Bill base model."""

    name: str = Field(
        min_length=2,
        max_length=16,
        description="Bill name must be 2-16 characters long.",
    )
    icon: str | None = None
    note: str | None = None
    amount: float = Field(
        ge=0,
        description="Amount must be a non-negative number.",
    )
    currency: Currency
    cycle: int = Field(
        ge=1,
        description="Cycle must be a positive integer.",
    )
    interval: Interval
    first_bill: str
    space_uuid: UUID
    category_uuid: UUID
    payers: list[Payer] | None = None


class BillIn(BillBase):
    """Bill request body model for bill creation and update."""

    pass


class BillOut(BillBase):
    """Bill response body model."""

    uuid: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
