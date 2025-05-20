from abc import ABC,abstractmethod
from ..base import Element

class Conversion(ABC):

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
    def getElementClassesThatCanConvertBy(cls, targetClass):
        """
        Return a list of all ElementBase subclasses that also inherit from Conversion
        and can convert to targetClass.
        """
        def all_subclasses(base):
            subclasses = set()
            for subclass in base.__subclasses__():
                subclasses.add(subclass)
                subclasses.update(all_subclasses(subclass))
            return subclasses

        result = []
        for subclass in all_subclasses(Element):
            if issubclass(subclass, Conversion) and subclass is not Conversion:
                if hasattr(subclass, "convertible") and callable(getattr(subclass, "convertible")):
                    if subclass.convertible(targetClass):
                        result.append(subclass)
        return result
