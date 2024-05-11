from datetime import datetime
from models import common
from pydantic import BaseModel, Field
from uuid import UUID


class BillBase(BaseModel):
    """
    Bill base model

    Attributes:
    - name: str
    - icon: emoji
    - note: str | None
    - amount: float
    - currency: ISO 4217 code
    - cycle: int
    - interval: "day" | "week" | "month" | "year"
    - first_bill: str
    - is_shared: bool
    """

    name: str = Field(
        min_length=2,
        max_length=16,
        description="Bill name must be 2-16 characters long.",
    )
    icon: str = Field(
        default="💸",
        pattern=r"[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U00002600-\U000027BF\U0001f300-\U0001f64F\U0001f680-\U0001f6C0\U0001f6c0-\U0001f6ff]",
        description="Invalid emoji icon.",
    )
    note: str | None = None
    amount: float = Field(
        ge=0,
        description="Amount must be a non-negative number.",
    )
    currency: common.Currency
    cycle: int = Field(
        ge=1,
        description="Cycle must be a positive integer.",
    )
    interval: common.Interval
    first_bill: datetime = Field(default=datetime.today)
    is_shared: bool = Field(default=False)


class BillIn(BillBase):
    """
    Bill input model

    Attributes:
    - name: str
    - icon: emoji
    - note: str | None
    - amount: float
    - currency: ISO 4217 code
    - cycle: int
    - interval: "day" | "week" | "month" | "year"
    - first_bill: str
    - is_shared: bool
    """

    pass


class BillOut(BillBase):
    """
    Bill output model

    Attributes:
    - uuid: UUID
    - name: str
    - icon: emoji
    - note: str | None
    - amount: float
    - currency: ISO 4217 code
    - cycle: int
    - interval: "day" | "week" | "month" | "year"
    - first_bill: str
    - payer_uuid: UUID
    - is_shared: bool
    - parent_uuid: UUID | None
    - category_uuid: UUID | None
    - status: "active" | "inactive"
    - created_at: datetime
    - updated_at: datetime
    """

    uuid: UUID
    payer_uuid: UUID
    parent_uuid: UUID | None
    category_uuid: UUID | None
    status: common.Status
    created_at: datetime
    updated_at: datetime
