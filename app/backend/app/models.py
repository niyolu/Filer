from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String, BigInteger, LargeBinary, BLOB
from sqlalchemy.orm import relationship

from database import Base, SerializableBase

import config


settings: config.Settings = config.get_settings()


user_group_table = Table(
    "user_group_table",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    
    quota = Column(BigInteger, default=(settings.storage_quota_mb * 1024**2))
    used = Column(BigInteger, default=0)
    max_objects_per_dir = Column(Integer, default=settings.storage_max_objects_per_dir)

    root_id = Column(Integer, ForeignKey("directories.id"))
    root = relationship("Directory", foreign_keys=[root_id], post_update=True)
    owned_objects = relationship("StorageObject", back_populates="owner", cascade="all, delete")
    
    group_memberships = relationship(
        "Group",
        secondary=user_group_table,
        back_populates="members"
    )
    
    shared_objects = relationship("StorageObject", secondary="storage_share", back_populates="shared_with_users")
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.id}, {self. username} root={self.root.name if self.root else 'None'})"
    
    def __str__(self):
        return f"{self!r} objects({self.owned_objects}=, {self.shared_objects}=) groups({self.group_memberships})"


class StorageObject(SerializableBase):
    __tablename__ = "storageobjects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    path = Column(String(255))
    
    type = Column(String(255))
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="owned_objects")
    
    # nullable parent_id since the root directory won't have a parent
    parent_id = Column(Integer, ForeignKey("directories.id"), nullable=True)
    parent = relationship(
        "Directory",
        back_populates="children",
        primaryjoin="StorageObject.parent_id == Directory.id"
    )
    
    shared_with_users = relationship("User", secondary="storage_share", back_populates="shared_objects")
    
    __mapper_args__ = {
        "polymorphic_identity": "storageobjects",
        "polymorphic_on": "type",
    }
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id=} {self.name=} {self.path=} owner={self.owner!r})"
    
    def __str__(self) -> str:
        return f"{self!r} parent = {self.parent!r}"
        

    
class File(StorageObject):
    __tablename__ = "files"
    
    id = Column(Integer, ForeignKey("storageobjects.id"), primary_key=True, index=True)
    
    filetype = Column(String(255))
    content = Column(LargeBinary(length=1024**3))
    
    __mapper_args__ = {
        "polymorphic_identity": "files",
        "polymorphic_on": "type",
    }
    
    def __repr__(self) -> str:
        return f"{super().__repr__().replace(super().__class__.__name__, self.__class__.__name__)} content({self.content}, {self.filetype=})"
    
    
class Directory(StorageObject):
    __tablename__ = "directories"
    
    id = Column(Integer, ForeignKey("storageobjects.id"), primary_key=True, index=True)
    
    children = relationship(
        "StorageObject",
        back_populates="parent",
        primaryjoin="Directory.id == StorageObject.parent_id",
    )
    
    __mapper_args__ = {
        "polymorphic_identity": "directories",
        "polymorphic_on": "type",
        "inherit_condition": id == StorageObject.id
    }
    
    def __repr__(self) -> str:
        return super().__repr__().replace(super().__class__.__name__, self.__class__.__name__)
    
    def __str__(self) -> str:
        return f"{self!r} children({','.join([str(child) for child in self.children])})"


class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    
    members = relationship(
        "User",
        secondary=user_group_table,
        back_populates="group_memberships"
    )
    
    shared_objects = relationship("StorageObject", secondary="group_share")
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id=} {self.name=})"
     
    def __str__(self) -> str:
        return f"{repr(self)} members({self.members}) shared_objects({self.shared_objects})" 


class StorageShare(Base):
    __tablename__ = "storage_share"
    
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    obj_id = Column(Integer, ForeignKey("storageobjects.id"), primary_key=True)
    
    permission = Column(String(10), default="R")
    
    
class GroupShare(Base):
    __tablename__ = "group_share"
    
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)
    obj_id = Column(Integer, ForeignKey("storageobjects.id"), primary_key=True)
    
    permission = Column(String(10), default="R")
