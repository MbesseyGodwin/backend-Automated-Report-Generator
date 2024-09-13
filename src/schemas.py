from pydantic import BaseModel, validator, EmailStr
from typing import List, Optional, Dict
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # Expect the plain password here, not the hash

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True

    @validator('created_at', 'updated_at', pre=True, always=True)
    def validate_dates(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v

class DataSourceCreate(BaseModel):
    source_name: str
    source_type: str
    connection_details: dict

class DataSourceOut(BaseModel):
    id: int
    source_name: str
    source_type: str
    connection_details: Dict  # Ensure this matches your JSON structure
    created_at: datetime

    class Config:
        orm_mode = True  # This tells Pydantic to use the ORM mode

# class ReportCreate(BaseModel):
#     title: str
#     description: str
#     data_source_ids: List[int]
#     template: str

class ReportCreate(BaseModel):
    title: str
    description: str
    # template: str
    user_id: int

    class Config:
        orm_mode = True

class ReportOut(BaseModel):
    id: int
    title: str
    description: str
    user_id: int
    created_at: str

    class Config:
        orm_mode = True

    @validator('created_at', pre=True, always=True)
    def validate_dates(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v

class TestConnection(BaseModel):
    source_id: int
