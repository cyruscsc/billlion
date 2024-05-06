from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

fake_users_db = {
    "johndoe": {"email": "johndoe@example.com", "password": "password"},
    "janedoe": {"email": "janedoe@example.com", "password": "password"},
}


class User(BaseModel):
    username: str
    email: str | None = None
    password: str


@router.post("/register")
async def register(user: User):
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=400,
            detail="Username already registered",
        )
    elif user.email in [user["email"] for user in fake_users_db.values()]:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )
    elif not user.password or len(user.password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password too short",
        )
    fake_users_db[user.username] = {"email": user.email, "password": user.password}
    return {
        "message": "Registered successfully",
        "username": user.username,
        "email": user.email,
    }


@router.post("/login")
async def login(user: User):
    if (
        user.username not in fake_users_db
        or fake_users_db[user.username]["password"] != user.password
    ):
        raise HTTPException(
            status_code=400,
            detail="Incorrect credentials",
        )
    return {
        "message": "Logged in successfully",
        "username": user.username,
        "email": fake_users_db[user.username]["email"],
    }


@router.get("/logout")
async def logout():
    return {
        "message": "Logged out successfully",
    }
