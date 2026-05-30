from app.infrastructure.adapters.security.hasher import Hasher
from app.infrastructure.persistence.models.user_model import UserModel

class UserService:
    def __init__(self, hasher: Hasher, user_model:UserModel ):
        self.hasher = hasher
        self.user_model = user_model

    def register(self, name, email, password):

        hashed_password = self.hasher.hash(password)
        self.user_model
        
