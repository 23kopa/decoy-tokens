from fastapi import Depends
from sqlalchemy.orm import Session
from backend.app.application.use_cases.user.register import RegisterUser
from backend.app.application.use_cases.user.authenticate import AuthenticateUser
from backend.app.infrastructure.database.repositories.user import SQLAlchemyUserRepository
from backend.app.core.security import hash_password, verify_password
from .db import get_db

def get_register_user(db: Session = Depends(get_db)) -> RegisterUser:
    repo = SQLAlchemyUserRepository(db)
    return RegisterUser(repo, hash_password)

def get_authenticate_user(db: Session = Depends(get_db)) -> AuthenticateUser:
    repo = SQLAlchemyUserRepository(db)
    return AuthenticateUser(repo, verify_password)