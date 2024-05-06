from fastapi import FastAPI
from routers import auth, bills, categories, spaces, users

app = FastAPI()
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(bills.router, prefix="/bills", tags=["bills"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(spaces.router, prefix="/spaces", tags=["spaces"])
app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/")
async def root():
    return {"message": "Hello World"}
