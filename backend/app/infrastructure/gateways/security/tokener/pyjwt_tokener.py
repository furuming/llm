import jwt
from app.domain.contracts.security.tokener import Tokener
from typing import Any

class PyJwtTokener(Tokener):

    def __init__(self, algorism: str, secret_key: str):
        self.algorism = algorism 
        self.secret_key = secret_key

    def encode(self, payload:dict[str, Any])->str:
        token = jwt.encode(payload,self.secret_key, algorithm=self.algorism)
        return token

    def decode(self, token:str )->dict[str, Any]:
        return jwt.decode(jwt=token, key=self.secret_key, algorithms=self.algorism)


