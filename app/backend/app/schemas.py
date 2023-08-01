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
    

class StorageObjectType(str, Enum):
    dir = "dir"
    file = "file"

    
class StorageDetails(BaseModel):
    owner: UserBase
    permission: Permission
    
    class Config:
        from_attributes = True
        

class StorageObjectBase(BaseModel):
    name: str
    path: str
    
    class Config:
        from_attributes = True
        

class FileBase(StorageObjectBase):
    filetype: str


class DirectoryBase(StorageObjectBase):
    pass


class FileCreate(FileBase):
    pass


class DirectoryCreate(DirectoryBase):
    pass


class OwnedFile(FileBase):
    pass


class OwnedDirectory(DirectoryBase):
    children: list[OwnedFile | OwnedDirectory]


class SharedStorageObject(StorageObjectBase, StorageDetails):
    pass


class SharedFile(SharedStorageObject):
    filetype: str
    

class SharedDirectory(SharedStorageObject):
    children: list[SharedFile | SharedDirectory] = []
    
    
class IterFile(SharedStorageObject):
    filetype: str
    

class IterDirectory(SharedStorageObject):
    pass


class StorageOverview(BaseModel):
    owned_objects: OwnedDirectory
    shared_objects: dict[str, list[SharedFile | SharedDirectory]] | None = None
    group_shared_objects: dict[str, list[SharedFile | SharedDirectory]] | None = None
    
    
class FullFile(SharedStorageObject):
    content: bytes


class Group(BaseModel):
    name: str
    members: list[UserBase]


class GroupWithShare(Group):
    shared: list[FileBase | DirectoryBase] | None
