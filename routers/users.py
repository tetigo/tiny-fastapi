from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from starlette import status
from .auth import get_current_user
from pydantic import Field, BaseModel
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Users).filter(Users.id == user.get("id")).first()


class UserUpdatePasswordRequest(BaseModel):
    password: str = Field(min_length=3)
    new_password: str = Field(min_length=3)


@router.put("/users", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_password(
    user: user_dependency, db: db_dependency, new_user: UserUpdatePasswordRequest
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    found_user = db.query(Users).filter(Users.id == user.get("id")).first()
    if found_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt_context.verify(new_user.password, found_user.hashed_password):
        raise HTTPException(status_code=401, detail="Authentication Failed")

    found_user.hashed_password = bcrypt_context.hash(new_user.new_password)
    db.add(found_user)
    db.commit()
