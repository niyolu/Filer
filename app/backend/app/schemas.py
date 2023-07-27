from pydantic import BaseModel


class User(BaseModel):
    username: str
    is_active: bool | None = None
    class Config:
        from_attributes = True
    

class UserInDB(User):
    hashed_password: str
    

class UserCreate(User):
    password: str
    

class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class TokenData(BaseModel):
    username: str | None = None


# sql tutorial


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass
