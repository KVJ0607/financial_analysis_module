from __future__ import annotations
from typing import Protocol,Iterator

from abc import ABC,abstractmethod



from typing import Type, TypeVar
T = TypeVar("T", bound="DataPoint")
E = TypeVar("E", bound="Element")


from .._date_utils import DateRepresentation

class DataPoint(ABC):        

    
    def __str__(self): 
        pass 
    
    
    @abstractmethod
    def __hash__(self):
        """Note that only int with preceding digits 20-99 is avaiable
        int with preceding digits 10-19 is reserved
        """
        pass

    @property
    @abstractmethod
    def date(self)->DateRepresentation:
        pass
              
    
                
    def valid(self)->bool:  
        return True 


 
    def toJson(self) -> dict:
        """
        Return a dictionary of all user-defined attributes (excluding private and built-in).
        Always includes 'id' and 'type_name' keys.
        """
        result = {
            "id": self.__hash__(),
            "type_name": self.__class__.__name__,
        }
        # Add all user-defined (non-private, non-callable) attributes
        for key, value in self.__dict__.items():
            if not key.startswith("_") and key not in result:
                result[key] = value
        return result    
    
    @classmethod
    @abstractmethod
    def correspondingGroupElement(cls)->type[E]:                        
        pass      

    @classmethod
    @abstractmethod
    def getGroupElement(cls,points:list[T])->E: 
        pass 
    
    





class Element(ABC): 

    
    @abstractmethod
    def __init__(self):
        pass 

    def __iter__(self)-> Iterator[DataPoint]:        
        return iter(self.dataPoints)
    
    def __len__(self): 
        """
        Return the number of DataPoint
        """    
        return len(self.dataPoints)
    
                                

    @property
    @abstractmethod
    def dataPoints(self)->list[T]:
        """
        Returns a list of DataPointBase objects contained in this Element.
        All subclasses must implement this property to return a list.
        """        
        pass
    

    
    
    @classmethod
    @abstractmethod
    def getPointType(cls)->Type[T]: 
        pass                                 


