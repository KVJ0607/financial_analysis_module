from abc import ABC,abstractmethod
from .base import ElementBase
class ConversionMixin(ABC):

    @abstractmethod
    def convertTo(self, targetTemplate):        
        pass
    
    @classmethod
    @abstractmethod
    def convertible(cls, targetClass):
        pass
    
    @classmethod
    @abstractmethod
    def getConvertibleClasses(cls):
        pass
    

    @classmethod
    def getClassThatCanConvertedTo(
        cls,
        targetClass):
        classes = []
        for subclass in cls.__subclasses__(): 
            if issubclass(subclass, ElementBase) and subclass.convertible(targetClass):
                classes.append(subclass)
        return classes           
