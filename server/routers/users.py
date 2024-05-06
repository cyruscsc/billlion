from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/me")
def read_users_me():
    return {
        "username": "fakecurrentuser",
    }
