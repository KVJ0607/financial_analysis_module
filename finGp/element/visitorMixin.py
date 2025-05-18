from abc import ABC,abstractmethod

class VisitorMixin(ABC):
    @abstractmethod
    def acceptVisitor(self, v):
        pass
    
    @abstractmethod
    def acceptOutVisitor(self, v, dest: str):
        pass
    

