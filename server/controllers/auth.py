import os
from sqlalchemy.orm import Session
from fastapi import HTTPException, Response, status

from ..helpers import verify_password, create_jwt, get_password_hash, validate_jwt
from ..model import UserModel
from ..schema import UserSignUpPayload, UserLoginPayload


def logout(res: Response):
    res.delete_cookie("authorization")
    return {"message": "Logout Successfull"}


def login(res: Response, db: Session, user: UserLoginPayload):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if user is None or not verify_password(
            user.password, db_user.hashed_password):  # type: ignore
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            "Invalid Credentials")

    jwt = create_jwt({"sub": db_user.id})  # type: ignore

    res.set_cookie("authorization",
                   jwt,
                   httponly=True,
                   secure=True,
                   samesite='none',
                   max_age=60 * 60 * 24 * 30)

    return {"message": "Login Successfull"}


def sign_up(res: Response, db: Session, user: UserSignUpPayload):
    hashed_password = get_password_hash(user.password)
    user_dict = user.model_dump()
    new_user = UserModel(full_name=user_dict["full_name"],
                         email=user_dict["email"],
                         hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    jwt = create_jwt({"sub": new_user.id})

    res.set_cookie("authorization",
                   jwt,
                   httponly=True,
                   secure=True,
                   samesite="none",
                   max_age=60 * 60 * 24 * 30)

    return {"message": "Sign Up Successfull"}


def is_user_authenticated(jwt: str):
    user_id = validate_jwt(jwt)
    if user_id is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not Logged in")
    return user_id
