from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    email: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserInDB(User):
    hashed_password: str

class UserOut(BaseModel):
    id: int
    email: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

class CSVFileBase(BaseModel):
    filename: str
    user_id: int
    file_content: bytes

class CSVFileCreate(CSVFileBase):
    pass

class CSVFile(CSVFileBase):
    id: int
    upload_time: datetime
    size: float
    user: User

    class Config:
        orm_mode = True

class CSVFileOut(BaseModel):
    id: int
    filename: str
    upload_time: datetime
    size: float
    user_id: int

class CSVFileInDB(CSVFile):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

