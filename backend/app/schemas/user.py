from datetime import date, datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=30, pattern=r"^\S+$")
    password: str = Field(min_length=8, max_length=72)  # bcrypt ignora/rechaza >72 bytes


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str
    avatar_url: str | None = None
    xp: int
    level: int
    current_streak: int
    longest_streak: int
    last_activity_date: date | None = None
    created_at: datetime


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefreshRequest(BaseModel):
    refresh_token: str
