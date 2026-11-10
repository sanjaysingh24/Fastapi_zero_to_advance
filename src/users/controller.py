from src.users.dtos import UserSchema
from sqlalchemy.orm import Session
from fastapi import HTTPException
from pwdlib import PasswordHash
from src.users.models import UserModel

password_hash = PasswordHash.recommended()


def gethashpass(password):
    return password_hash.hash(password)


def register(body: UserSchema, db: Session):

    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user:
        raise HTTPException(400, detail="Username already exists")
    is_email = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_email:
        raise HTTPException(400, detail="Email already exists")
    hash_password = gethashpass(body.password)
    new_user = UserModel(
        name=body.name,
        username=body.username,
        email=body.email,
        hash_password=hash_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
