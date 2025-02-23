from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class User(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    gender: str = Field(..., min_length=1, max_length=6)
    email: EmailStr
    age: Optional[int] = Field(None, ge=0, le=120)
    is_active: bool = True
