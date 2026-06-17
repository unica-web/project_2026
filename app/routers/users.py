from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select

from app.models.user import User
from app.models.registration import Registration
from app.data.db import get_session

user_router = APIRouter(
    prefix="/users",
)

@user_router.get("")
def get_user(session: Session = Depends(get_session)):
    users=session.exec(select(User)).all()
    return users

@user_router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user_in: User,session: Session = Depends(get_session)):
    db_users=session.get(User,user_in.username)
    if db_users:
        raise HTTPException(status_code=400, detail="Username already exists")
