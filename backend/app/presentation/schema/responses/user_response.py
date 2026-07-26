from pydantic import BaseModel, EmailStr, Field


class CreateUserResponse(BaseModel):
    name: str
    email: EmailStr
    access_token: str = Field(exclude=True)


class LoginResponse(BaseModel):
    name: str
    email: EmailStr
    access_token: str = Field(exclude=True)


class AuthenticatedUserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
