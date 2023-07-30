from __future__ import annotations

from typing import ForwardRef, Optional
from pydantic import BaseModel
from enum import Enum

class UserBase(BaseModel):
    username: str
    is_active: bool | None = None
    
    class Config:
        from_attributes = True

class User(UserBase):
    quota: int
    used: int


class UserInDB(User):
    id: int
    hashed_password: str
    

class UserCreate(UserBase):
    password: str
    

class Token(BaseModel):
    access_token: str
    token_type: str
    quota: int | None = None
    used: int | None = None
    
    
class TokenData(BaseModel):
    username: str | None = None


class Permission(str, Enum):
    R = "R"
    RW = "RW"


Directory_Ref = ForwardRef("Directory")

class StorageObjectType(str, Enum):
    R = "R"
    RW = "RW"


class StorageObjectBase(BaseModel):
    name: str
    path: str
    
    class Config:
        from_attributes = True

class StorageObject(StorageObjectBase):
    owner: User | None = None
    permission: Permission | None = None
    #parent: Directory | None # Optional[Directory_Ref] # "Optional[Directory]" 


class FileSummary(StorageObjectBase):
    filetype: str | None = None


class DirectorySummary(StorageObjectBase):
    pass

class DirectorySummaryChildren(DirectorySummary):
    children: list[FileSummary | DirectorySummaryChildren]
    

class File(StorageObject):
    filetype: str | None = None
    #content: bytes


class Directory(StorageObject):
    children: list[File | Directory]


class StorageObjectCreate(BaseModel):
    path: str
    name: str


class FileCreate(StorageObjectCreate):
    content: bytes

    
class FileOverview(BaseModel):
    owned_files: DirectorySummaryChildren
    shared_objects: list[Directory | File]
    group_shared_objects: dict[str, list[Directory | File]]


class DirectoryCreate(StorageObjectCreate):
    pass


class Group(BaseModel):
    name: str
    members: list[User]


class GroupWithShare(Group):
    shared: list[File | Directory] | None
