from pydantic import BaseModel, EmailStr

class UserInput(BaseModel):
    name: str
    email: EmailStr
    password: str
