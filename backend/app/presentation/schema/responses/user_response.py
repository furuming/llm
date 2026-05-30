from pydantic import BaseModel, EmailStr


class CreateUserResponse(BaseModel):
    name: str
    email: EmailStr
