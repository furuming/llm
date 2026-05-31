from pydantic import BaseModel, EmailStr

class UserOutput(BaseModel):
    id: str
    name: str
    email: EmailStr
    jwt: str
