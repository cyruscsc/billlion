from database import SessionLocal
from datetime import datetime
from models import category, database, user
from sqlalchemy.orm import Session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_user(db: Session, user: user.UserInWithInfo):
    db_user = database.User(
        username=user.username,
        email=user.email,
        hashed_password=user.password,
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


def create_category(db: Session, category: category.CategoryInWithOwner):
    db_category = database.Category(
        name=category.name,
        icon=category.icon,
        owner_uuid=category.owner_uuid,
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category(db: Session, category_uuid: str):
    return (
        db.query(database.Category)
        .filter(database.Category.uuid == category_uuid)
        .first()
    )


def update_category(
    db: Session,
    db_category: database.Category,
    category: category.CategoryInWithoutOwner,
):
    db_category.name = category.name
    db_category.icon = category.icon
    db_category.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_category)
    return db_category


def deactivate_category(db: Session, db_category: database.Category):
    db_category.status = "inactive"
    db_category.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_category)
    return db_category
