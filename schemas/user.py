from pydantic import BaseModel, EmailStr

# What we expect when someone REGISTERS
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# What we RETURN (never return password!)
class UserOut(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        from_attributes = True

# Login request
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# JWT token response
class Token(BaseModel):
    access_token: str
    token_type: str