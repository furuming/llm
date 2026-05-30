import bcrypt
from app.infrastructure.adapters.security.hasher import Hasher


class BcryptHasher(Hasher):

    def hash(self, text:str)->str:
        return bcrypt.hashpw( text.encode("utf-8"), bcrypt.gensalt() ).decode("utf-8")


        

    def verify(self, text:str, hashed:str)->bool:
        return bcrypt.checkpw(text.encode("utf-8"), hashed_password=hashed.encode("utf-8"))


