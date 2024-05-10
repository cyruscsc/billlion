from database import SessionLocal
from models import body, database
from sqlalchemy.orm import Session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_user(db: Session, user: body.UserIn):
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


def create_space(db: Session, space: body.SpaceIn, user_uuid: str):
    db_space = database.Space(name=space.name, icon=space.icon)
    db.add(db_space)
    db.commit()
    db_space_user = database.SpaceUser(
        space_uuid=db_space.uuid,
        user_uuid=user_uuid,
        role=database.Role.owner,
    )
    db.add(db_space_user)
    db.commit()
    db.refresh(db_space_user)
    db.refresh(db_space)
    return db_space


def get_space(db: Session, space_uuid: str):
    return db.query(database.Space).filter(database.Space.uuid == space_uuid).first()


def get_space_user(db: Session, space_uuid: str, user_uuid: str):
    return (
        db.query(database.SpaceUser)
        .filter(database.SpaceUser.space_uuid == space_uuid)
        .filter(database.SpaceUser.user_uuid == user_uuid)
        .first()
    )


def update_space_user_role(
    db: Session, space_uuid: str, user_uuid: str, role: database.Role
):
    db_space_user = get_space_user(db, space_uuid, user_uuid)
    db_space_user.role = role
    db.commit()
    db.refresh(db_space_user)
    return db_space_user
