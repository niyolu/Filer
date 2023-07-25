from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(255), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
    
# class DBA(Base):
#     __tablename__ = "DBA"
#     i = Column(Integer, primary_key=True, index=True)
#     n = Column(String(255), index=True)
    
# class A(BaseModel):
#     i: int
#     n: str
#     class Config:
#         from_attributes = True
    
# a = DBA(i=1, n="hi")
# print(a)
# b = A.model_validate(a)
# print(b)
# print(DBA(**b.model_dump()))
