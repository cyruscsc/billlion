from dependencies import crud
from fastapi import APIRouter, Depends, HTTPException
from models import category
from sqlalchemy.orm import Session
from uuid import UUID

router = APIRouter()
# TODO: Find better solution for "Value must be a Guid" error


@router.post("/", response_model=category.CategoryOutBrief)
async def create_category(
    category: category.CategoryInWithOwner, db: Session = Depends(crud.get_db)
):
    return crud.create_category(db, category=category)


@router.get("/{category_uuid}", response_model=category.CategoryOutBrief)
async def read_category(category_uuid: str, db: Session = Depends(crud.get_db)):
    # Workaround for "Value must be a Guid" error
    db_category = crud.get_category(db, category_uuid=UUID(category_uuid))
    if db_category is None or db_category.status == "inactive":
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.get("/user/{user_uuid}", response_model=list[category.CategoryOutBrief])
async def read_categories_by_user(user_uuid: str, db: Session = Depends(crud.get_db)):
    # Workaround for "Value must be a Guid" error
    db_user = crud.get_user(db, user_uuid=UUID(user_uuid))
    if db_user is None or db_user.status == "inactive":
        raise HTTPException(status_code=404, detail="User not found")
    return filter(lambda x: x.status == "active", db_user.categories)


@router.put("/{category_uuid}", response_model=category.CategoryOutBrief)
async def update_category(
    category_uuid: str,
    category: category.CategoryInWithoutOwner,
    db: Session = Depends(crud.get_db),
):
    # Workaround for "Value must be a Guid" error
    db_category = crud.get_category(db, category_uuid=UUID(category_uuid))
    if db_category is None or db_category.status == "inactive":
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.update_category(db, db_category=db_category, category=category)


@router.delete("/{category_uuid}", response_model=category.CategoryOutBrief)
async def delete_category(category_uuid: str, db: Session = Depends(crud.get_db)):
    # Workaround for "Value must be a Guid" error
    db_category = crud.get_category(db, category_uuid=UUID(category_uuid))
    if db_category is None or db_category.status == "inactive":
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.deactivate_category(db, db_category=db_category)
