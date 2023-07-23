from sqlalchemy.orm import Session

from typing import Annotated
from fastapi import Depends

from . import models, schemas, auth


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.User)
        .order_by(models.User.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.fake_hash_password(user.password)
    db_user = models.User(
        email=user.username, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Item)
        .order_by(models.Item.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def fake_decode_token(token):
    return schemas.User(
        username=token + "fakedecoded"
    )
    
async def get_current_user(token: Annotated[str, Depends(auth.oauth2_scheme)]):
    user = fake_decode_token(token)
    return user
