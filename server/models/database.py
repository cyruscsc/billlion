import uuid
from database import Base
from datetime import datetime
from models import common
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    Integer,
    ForeignKey,
    String,
    Uuid,
)
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    uuid = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    display_name = Column(String)
    status = Column(Enum(common.Status), default=common.Status.active)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    bills = relationship("Bill", back_populates="payer")


class Category(Base):
    __tablename__ = "categories"

    uuid = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, default="New Category")
    icon = Column(String, default="📦")
    status = Column(Enum(common.Status), default=common.Status.active)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    bills = relationship("Bill", back_populates="category")


class Bill(Base):
    __tablename__ = "bills"

    uuid = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, default="New Bill")
    icon = Column(String, default="💸")
    note = Column(String)
    amount = Column(Float, default=0)
    currency = Column(Enum(common.Currency), default=common.Currency.cad)
    cycle = Column(Integer, default=1)
    interval = Column(Enum(common.Interval), default=common.Interval.month)
    first_bill = Column(DateTime, default=datetime.today)
    payer_uuid = Column(Uuid, ForeignKey("users.uuid"))
    is_shared = Column(Boolean, default=False)
    parent_uuid = Column(Uuid, ForeignKey("bills.uuid"), nullable=True)
    category_uuid = Column(Uuid, ForeignKey("categories.uuid"), nullable=True)
    status = Column(Enum(common.Status), default=common.Status.active)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    payer = relationship("User", back_populates="bills")
    category = relationship("Category", back_populates="bills")
    parent = relationship("Bill", back_populates="children", remote_side=[uuid])
    children = relationship("Bill", back_populates="parent")
