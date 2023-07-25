from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = token
    return user


def fake_hash_password(password: str):
    return "fakehashed" + password