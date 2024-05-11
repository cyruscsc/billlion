from database import Base, engine, SessionLocal
from fastapi import FastAPI
from routers import auth, bills, categories, users

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(bills.router, prefix="/bills", tags=["bills"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/")
async def root():
    return {"message": "Hello World"}
