from passlib.context import CryptContext
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer

from jose import jwt

from . import crud, models, config, schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

settings = config.get_settings()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db, username: str, password: str):
    user: models.User = crud.get_user_by_username(db, username)
    if not user:
        return False
    print(password, user.hashed_password)
    if not verify_password(password, user.hashed_password):
        return False
    return schemas.User.model_validate(user)


def create_access_token(data: dict, expires_delta: int | None = None):
    to_encode = data.copy()
    if not expires_delta:
        expires_delta = settings.auth_access_token_expire_minutes
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.auth_secret_key, algorithm=settings.auth_algorithm)
    return encoded_jwt


def decode_token(token: str):
    payload = jwt.decode(token, settings.auth_secret_key, algorithms=[settings.auth_algorithm])
    username: str = payload.get("sub")
    if username is not None:
        return schemas.TokenData(username=username)