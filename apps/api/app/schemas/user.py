
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, ConfigDict


# --------------------------------------------------
# 1. CREATE USER SCHEMA
# --------------------------------------------------

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)


# --------------------------------------------------
# 2. LOGIN SCHEMA
# --------------------------------------------------

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# --------------------------------------------------
# 3. USER RESPONSE SCHEMA
# --------------------------------------------------

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role_id: UUID
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --------------------------------------------------
# 4. UPDATE USER STATUS SCHEMA
# --------------------------------------------------

class UserStatusUpdate(BaseModel):
    is_active: bool
