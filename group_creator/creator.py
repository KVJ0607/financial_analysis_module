from abc import ABC,abstractmethod

class Creator(ABC): 
    
    @classmethod
    @abstractmethod
    def getInstacnefrom(cls,fileName=str):
        pass 
        