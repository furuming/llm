from pydantic import BaseModel, EmailStr


class CreateUserResponse(BaseModel):
    name: str
    email: EmailStr
    access_token: str

class LoginResponse(BaseModel):
    name: str
    email: EmailStr
    access_token: str
