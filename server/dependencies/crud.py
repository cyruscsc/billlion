from database import SessionLocal
from models import database, user
from sqlalchemy.orm import Session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_user(db: Session, user: user.UserInComplete):
    hashed_password = user.password + "notreallyhashed"
    db_user = database.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        display_name=user.display_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_uuid: str):
    return db.query(database.User).filter(database.User.uuid == user_uuid).first()


def get_user_by_username(db: Session, username: str):
    return db.query(database.User).filter(database.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(database.User).filter(database.User.email == email).first()
