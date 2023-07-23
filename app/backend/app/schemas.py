from pydantic import BaseModel


class User(BaseModel):
    username: str
    disabled: bool | None = None
    

class UserInDB(User):
    hashed_password: str
    
    
class UserCreate(User):
    password: str


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         from_attributes = True


# class UserBase(BaseModel):
#     username: str
#     disabled: bool | None = None
    



# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     items: list[Item] = []

#     class Config:
#         from_attributes = True
