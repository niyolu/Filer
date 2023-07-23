from fastapi.security import OAuth2PasswordBearer

from . import crud


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_decode_token(db, token):
    # This doesn't provide any security at all
    # Check the next version
    username = token.username
    user = crud.get_user(db, username)
    return user


def fake_hash_password(password: str):
    return "fakehashed" + password