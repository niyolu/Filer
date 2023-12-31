from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status, UploadFile, Response, Request, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from sqlalchemy.orm import Session

from jose import JWTError

from logger import logger

import crud, models, schemas, auth, database


models.Base.metadata.create_all(bind=database.engine)

LocalSession = Annotated[Session, Depends(database.get_db)]

crud.init_admin(next(database.get_db()))

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

router_user = APIRouter(prefix="/users", tags=["users"])
router_storage = APIRouter(prefix="/storage", tags=["storage"])
router_groups = APIRouter(prefix="/groups", tags=["groups"])
router_shared = APIRouter(prefix="/shares", tags=["shares"])


@app.get("/logtest")
async def read_root():
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
    return {"message": "Hello, World!"}


@app.get("/")
def healthcheck():
    return "running"


@app.exception_handler(PermissionError)
async def permission_exception_handler(request: Request, exc: PermissionError):
    logger.warn(str(exc))
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"message": f"Oopsie! {exc} did a happening."},
    
    )

@app.exception_handler(ValueError)
async def valueerror_exception_handler(request: Request, exc: ValueError):
    logger.warn(str(exc))
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": f"Oopsie! {exc} did a happening."},
    )

@app.exception_handler(crud.DuplicateError)
async def duplicate_exception_handler(request: Request, exc: crud.DuplicateError):
    logger.warn(str(exc))
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": f"Oopsie! {exc} did a happening."},
    )
    
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, KeyboardInterrupt):
        raise exc
    logger.warn(str(exc))
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": f"Oopsie! {exc} did a happening."},
    )


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
            logger.warn(credentials_exception)
            raise credentials_exception
    except JWTError:
        logger.warn(credentials_exception)
        raise credentials_exception
    user = crud.get_user_by_username(db, token_data.username)
    if not user:
        logger.warn(credentials_exception)
        raise credentials_exception
    
    return schemas.User.model_validate(user)


async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    if not current_user.is_active:
        logger.warn("inactive user")
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_admin(
    current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    if not current_user.username == "root":
        logger.warn("Invalid action 401 UNAUTHORIZED")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid action",
        )
        
    return current_user


CurrentUser = Annotated[schemas.User, Depends(get_current_active_user)]
Admin = Annotated[schemas.User, Depends(get_admin)]


@app.post("/token", response_model=schemas.Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: LocalSession
):
    user: schemas.User = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warn("Incorrect username or password Invalid action 401 UNAUTHORIZED")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username}) # data should be in auth api not here
    return {"access_token": access_token, "token_type": "bearer"}


@router_user.get("/me", response_model=schemas.User)
async def read_users_me(
    current_user: CurrentUser
):
    return current_user


@router_user.get("/", response_model=list[schemas.UserBase])
def read_users(
    db: LocalSession
):
    return crud.get_users(db)


@router_user.post("/", response_model=tuple[schemas.User, str])
def create_user(
    user: schemas.UserCreate,
    db: LocalSession
):
    hashed_password = auth.get_password_hash(user.password)
    db_user = crud.create_user(db=db, username=user.username, hashed_password=hashed_password)
    if not db_user:
        logger.warn("Incorrect username or password Invalid action 400 BAD REQUEST")
        raise Exception("User already registered")
    access_token = auth.create_access_token(data={"sub": db_user.username})
    return db_user, access_token


@router_user.delete("/", response_model=schemas.User)
def delete_user(
    current_user: CurrentUser,
    db: LocalSession
):
    user = crud.get_user_by_username(db, current_user.username)
    db_user = crud.delete_user(db, user.id)
    return db_user


@router_user.post("/deactivate", response_model=schemas.User)
def deactivate_user(
    current_user: CurrentUser,
    db: LocalSession
):
    return crud.change_active_status_for_user_by_username(db, current_user.username, False)


@router_user.post("/activate", response_model=schemas.User)
def activate_user(
    admin: Admin,
    username: str,
    db: LocalSession
):    
    return crud.change_active_status_for_user_by_username(db, username, True)


@router_user.post("/quota", response_model=schemas.User)
def change_quota(
    admin: Admin,
    username: str,
    new_quota: int,
    db: LocalSession
):    
    return crud.change_user_quota(db, username, new_quota)


@router_groups.get("/groups", response_model=list[schemas.Group])
def read_groups(
    db: LocalSession
):
    return crud.get_groups(db)


@router_groups.get("/me", response_model=list[schemas.Group])
def read_my_groups(
    current_user: CurrentUser,
    db: LocalSession
):
    return crud.get_group_by_username(db, current_user.username)


@router_groups.post("/", response_model=schemas.Group)
def create_group(
    admin: Admin,
    db: LocalSession,
    group_name: str
):
    return crud.create_group(db, group_name)


@router_groups.patch("/join", response_model=schemas.Group)
def add_user_to_group(
    admin: Admin,
    db: LocalSession,
    group_name: str,
    user_name: str
):
    group_id = crud.get_group_by_groupname(db, group_name).id
    user_id = crud.get_user_by_username(db, user_name).id
    return crud.add_user_to_group(db, group_id, user_id)


@router_storage.get("/", response_model=schemas.StorageOverview)
def read_files(
    current_user: CurrentUser,
    db: LocalSession
):
    user = crud.get_user_by_username(db, current_user.username)
    return crud.get_all_objs_tree(db, user.id)


@router_storage.post("/file", response_model=schemas.FileCreate)
async def upload_file(
    current_user: CurrentUser,
    db: LocalSession,
    file: UploadFile,
    path: str
):
    user= crud.get_user_by_username(db, current_user.username)

    filename = file.filename
    content = await file.read()
    # content = file.file.read()
    
    logger.debug(f"Received upload {filename} ({str(len(content) / 1024)} kiB) target={path}")
    
    res = crud.create_storage_object(db, user.id, path, filename, content=content)
    
    if not res:
        logger.debug("obj" + filename + "already exists")
    
    return res


@router_storage.post("/directory", response_model=schemas.DirectoryBase)
async def create_directory(
    current_user: CurrentUser,
    db: LocalSession,
    directory: schemas.DirectoryCreate
):
    user = crud.get_user_by_username(db, current_user.username)
    
    return crud.create_storage_object(db, user.id, directory.path, directory.name)


@router_storage.delete("/", response_model=list[schemas.OwnedFile | schemas.OwnedDirectory])
async def delete_object(
    current_user: CurrentUser,
    db: LocalSession,
    path: str,
):
    user = crud.get_user_by_username(db, current_user.username)
    return crud.delete_object_by_path(db, user.id, path)


class BytesResponse(Response):
    def __init__(self, content: bytes, filename: str = None, status_code: int = 200):
        media_type = "application/octet-stream"
        headers = {}
        if filename:
            headers["Content-Disposition"] = f'attachment; filename="{filename}"'
        super().__init__(content=content, media_type=media_type, headers=headers, status_code=status_code)


@router_storage.post("/download", response_class=BytesResponse)
async def download_object(
    current_user: CurrentUser,
    db: LocalSession,
    path: str
):
    user: models.User = crud.get_user_by_username(db, current_user.username)
    file: models.StorageObject = crud.get_storageobject_by_path(db, user.id, path)
    if not isinstance(file, models.File):
        logger.warn("resource is not a file")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="resource is not a file")
    
    return BytesResponse(content=file.content, filename=file.name)


@router_shared.post("/user")
def share_with_user(
    current_user: CurrentUser,
    db: LocalSession,
    user_name: str,
    path: str,
    permission: schemas.Permission
):
    from_user= crud.get_user_by_username(db, current_user.username)
    to_user = crud.get_user_by_username(db, user_name)
    obj_id = crud.get_storageobject_id_by_path(db, from_user.id, path)
    crud.share_storage_object_with_user(db, obj_id, from_user.id, to_user.id, permission.value)
    
    
@router_shared.post("/group")
def share_with_group(
    current_user: CurrentUser,
    db: LocalSession,
    group_name: str,
    path: str,
    permission: schemas.Permission
):
    user = crud.get_user_by_username(db, current_user.username)
    group = crud.get_group_by_groupname(db, group_name)
    obj_id = crud.get_storageobject_id_by_path(db, user.id, path)
    crud.share_storage_object_with_group(db, obj_id, group.id, permission.value)


app.include_router(router_user)
app.include_router(router_storage)
app.include_router(router_groups)
app.include_router(router_shared)
