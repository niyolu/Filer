from __future__ import annotations

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

class StorageObjectType(str, Enum):
    R = "R"
    RW = "RW"


class StorageObject(BaseModel):
    name: str
    path: str
    type: str
    
    owner: User | None = None
    
    #parent: Directory | None # Optional[Directory_Ref] # "Optional[Directory]" 
    
    permission: Permission | None = None
    
    class Config:
        from_attributes = True
        

class StorageObjectDBID(StorageObject):
    id: int
    

class File(StorageObject):
    filetype: str | None = None
    content: bytes


class FileDBID(StorageObject):
    pass


class DirectoryDBID(StorageObject):
    pass


class Directory(StorageObject):
    children: list[File | Directory]


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
