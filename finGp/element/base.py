from __future__ import annotations
from abc import ABC,abstractmethod


from ..date_utils.dateRepresentation import DateRepresentation

class DataPointBase(ABC):        

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
    
    @property
    @abstractmethod
    def correspondingGroupElement(self)->type[ElementBase]:                        
        pass        

                
    @abstractmethod
    def valid(self)->bool:  
        pass 
    

    @classmethod
    @abstractmethod
    def getGroupElement(cls,points:list['DataPointBase'])->ElementBase: 
        pass 
    
    @classmethod
    @abstractmethod
    def getTypeGroupElement(cls)->type[ElementBase]:
        pass 





class ElementBase(ABC): 

    def __len__(self): 
        """
        Return the number of DataPoint
        """    
        return len(self.dataPoints)
    
    @property
    @abstractmethod
    def pointType(self)->type[DataPointBase]: 
        pass                             



    @property
    @abstractmethod
    def dataPoints(self):
        pass
    
                            


