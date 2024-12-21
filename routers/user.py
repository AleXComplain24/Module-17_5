from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated, List
from app.models import User
from app.schemas import CreateUser, UpdateUser, UserResponse
from sqlalchemy import select, insert, update, delete

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
async def all_users(db: Annotated[Session, Depends(get_db)]):
    stmt = select(User)
    users = db.scalars(stmt).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    stmt = select(User).where(User.id == user_id)
    user = db.scalar(stmt)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    return user

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    stmt = insert(User).values(**user.dict())
    db.execute(stmt)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put("/update/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    stmt = update(User).where(User.id == user_id).values(**user.dict())
    result = db.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}

@router.delete("/delete/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    stmt = delete(User).where(User.id == user_id)
    result = db.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User deletion is successful!'}
