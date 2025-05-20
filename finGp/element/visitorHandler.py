from abc import ABC,abstractmethod

class VisitorHandler(ABC):
    
    @abstractmethod
    def acceptVisitor(self,v):
        pass
    
    @abstractmethod
    def acceptOutVisitor(self,v, dest: str):
        pass
    

