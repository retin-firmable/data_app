from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str

class UserType(BaseModel):
    type: str


class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True


class CSVFileBase(BaseModel):
    filename: str
    user_id: int


class CSVFileCreate(CSVFileBase):
    file_content: bytes


class CSVFile(CSVFileBase):
    id: int
    upload_time: datetime
    size: float
    user: User

    class Config:
        orm_mode = True

class CSVFileUpdate(CSVFileBase):
    filename: Optional[str] = None
    user_id: Optional[int] = None

class CSVFileOut(BaseModel):
    id: int
    filename: str
    upload_time: datetime
    size: float
    user_id: int

    