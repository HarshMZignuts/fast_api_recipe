from pydantic import BaseModel,Field,EmailStr,field_validator,model_validator
from uuid import UUID
import re

class UserCreate(BaseModel):
    user_name: str = Field(...,min_length=3,max_length=15)
    first_name: str = Field(...,min_length=3,max_length=15)
    last_name: str = Field(...,min_length=3,max_length=15)
    phone_code: str = Field(...,pattern=r"^\+[1-9]\d{0,3}$",
    description="Country calling code (e.g., +91, +1, +44)")
    phone_number: str = Field(...,pattern=r"^[1-9]\d{9,14}$",
    description="Phone number without country code")
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        max_length=20,
    
    )
    confirm_password:str = Field(...,
        min_length=8,
        max_length=20,
        description="Must match password")
    # Strip all string fields BEFORE validation
    @field_validator("*", mode="before")
    def strip_strings(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v
    # Username validation AFTER stripping
    @field_validator("user_name")
    def validate_username(cls, v):
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username can only contain letters, numbers, underscore")
        return v
    # Password fild validator
    @field_validator("password")
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Must contain at least one number")
        if not re.search(r"[@$!%*?&]", v):
            raise ValueError("Must contain at least one special character")
        return v
    # Match password & confirm_password
    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
      


class UserResponse(BaseModel):
    id: UUID
    user_name: str
    first_name: str
    last_name: str
    phone_number: str
    email: str

    class Config:
        from_attributes = True 
