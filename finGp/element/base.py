from __future__ import annotations
from abc import ABC,abstractmethod

from .visitorHandler import VisitorHandler

from typing import Type, TypeVar
T = TypeVar("T", bound="DataPoint")
E = TypeVar("E", bound="Element")


from .._date_utils.dateRepresentation import DateRepresentation

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
          

                
    @abstractmethod
    def valid(self)->bool:  
        pass 

    @classmethod
    @abstractmethod
    def correspondingGroupElement(cls)->type[E]:                        
        pass      

    @classmethod
    @abstractmethod
    def getGroupElement(cls,points:list[T])->E: 
        pass 
    






class Element(ABC): 

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
    
    @property
    @abstractmethod
    def visitorHandler(self)->Type[VisitorHandler]:
        pass
    
    
    @classmethod
    @abstractmethod
    def pointType(cls)->Type[T]: 
        pass                                 


