from dependencies import crud
from fastapi import APIRouter, Depends, HTTPException
from models import body
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/register", response_model=body.UserOut)
async def register(user: body.UserRegister, db: Session = Depends(crud.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered",
        )
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )
    return crud.create_user(db, user=user)


@router.post("/login", response_model=body.UserOut)
def login(user: body.UserLogin, db: Session = Depends(crud.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if not db_user or db_user.hashed_password != user.password + "notreallyhashed":
        raise HTTPException(
            status_code=400,
            detail="Incorrect credentials",
        )
    return db_user


@router.get("/logout")
async def logout():
    return {
        "message": "Logged out successfully",
    }
