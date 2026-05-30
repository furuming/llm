
class AuthController:
    def __init__(self):
        pass

    async def test(self)->str:
        print("test")
        return "test"
    
    async def create(self):
        print("register")
        return "register"