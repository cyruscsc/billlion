import datetime, enum, uuid
from database import Base
from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    Uuid,
)
from sqlalchemy.orm import relationship


class Status(str, enum.Enum):
    active = "active"
    inactive = "inactive"


class User(Base):
    __tablename__ = "users"

    uuid = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    display_name = Column(String)
    status = Column(Enum(Status), default=Status.active)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    spaces = relationship("Space", secondary="space_user", back_populates="users")


class Space(Base):
    __tablename__ = "spaces"

    uuid = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True)
    icon = Column(String)
    status = Column(Enum(Status), default=Status.active)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", secondary="space_user", back_populates="spaces")


space_user = Table(
    "space_user",
    Base.metadata,
    Column("space_uuid", Uuid, ForeignKey("spaces.uuid"), primary_key=True),
    Column("user_uuid", Uuid, ForeignKey("users.uuid"), primary_key=True),
)
