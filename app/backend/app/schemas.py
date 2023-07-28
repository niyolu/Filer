from typing import ForwardRef, Optional
from pydantic import BaseModel
from enum import Enum

class User(BaseModel):
    username: str
    is_active: bool | None = None
    
    quota: int
    used: int
    
    class Config:
        from_attributes = True
    

class UserInDB(User):
    id: int
    hashed_password: str
    

class UserCreate(User):
    password: str
    

class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class TokenData(BaseModel):
    username: str | None = None


class Permission(str, Enum):
    R = "R"
    RW = "RW"


Directory_Ref = ForwardRef("Directory")


class StorageObject(BaseModel):
    name: str
    path: str
    type: str
    
    owner: User
    
    parent: Optional[Directory_Ref]
    
    permission: Permission
    

class File(StorageObject):
    filetype: str
    content: bytes

   
class Directory(StorageObject):
    children: list[StorageObject]


class StorageObjectCreate(BaseModel):
    destination: str
    owner: User
    name: str


class FileCreate(StorageObjectCreate):
    content: bytes


class DirectoryCreate(BaseModel):
    pass


class Group(BaseModel):
    name: str
    members: list[User]
