from abc import ABC, abstractmethod

class HasherContract(ABC):

    @abstractmethod
    def hash(self, text:str)->str:
        pass


    @abstractmethod
    def verify(self, text:str, hashed:str)->bool:
        pass


