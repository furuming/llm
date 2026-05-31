from dataclasses import dataclass


@dataclass
class User:
    id: str | None
    email: str
    name: str
    password: str
    
