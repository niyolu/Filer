from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from jose import JWTError

from . import crud, models, schemas, auth, database
from .database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    # Add your frontend domain(s) here to restrict CORS to specific domains
    "http://localhost:3000",  # Example: Replace with your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LocalSession = Annotated[Session, Depends(database.get_db)]


async def get_current_user(
    token: Annotated[str, Depends(auth.oauth2_scheme)],
    db: LocalSession
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_data: schemas.TokenData | None = auth.decode_token(token)
        if token_data is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, token_data.username)
    if not user:
        raise credentials_exception
    
    return schemas.User.model_validate(user)


async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


CurrentUser = Annotated[schemas.User, Depends(get_current_active_user)]


@app.post("/token", response_model=schemas.Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: LocalSession
):
    user: schemas.User = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username}) # should be in auth api not here
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=schemas.User)
async def read_users_me(
    current_user: CurrentUser
):
    return current_user


@app.post("/users", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,
    db: LocalSession
):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)


@app.post("/users/deactivate/")
def deactivate_user(
    current_user: CurrentUser,
    db: LocalSession
):
    return crud.deactivate_user_by_username(db, current_user.username)


@app.post("/users/activate/")
def activate_user(
    current_user: CurrentUser,
    db: LocalSession
):
    if not auth.is_admin(current_user.username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid action",
        )
        
    return crud.deactivate_user_by_username(db, current_user.username)


@app.get("/")
def root():
    return "running"


@app.get("/storage/all")
def read_own_files(
    current_user: CurrentUser,
    db: LocalSession
):
    user: models.User = crud.get_user_by_username(db, current_user.username)
    root_dir = {"id": "/root", "children": ["foo.txt", "bar.txt"], "owner": user.username} # user.files or something
    return root_dir

# @app.get("/users/", response_model=List[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items


# @app.get("/items/")
# async def read_items(token: Annotated[str, Depends(auth.oauth2_scheme)]):
#     print(token)
#     return {"token": token}
