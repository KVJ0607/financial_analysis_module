from __future__ import annotations
from abc import ABC,abstractmethod


from ..date_utils.dateRepresentation import DateRepresentation

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

    @property
    @abstractmethod
    def correspondingGroupElement(self)->type[Element]:                        
        pass        
    
                
    @abstractmethod
    def valid(self)->bool:  
        pass 

    

    @classmethod
    @abstractmethod
    def getGroupElement(cls,points:list['DataPoint'])->Element: 
        pass 
    
    @classmethod
    @abstractmethod
    def getTypeGroupElement(cls)->type[Element]:
        pass 





class Element(ABC): 
    
    @property
    @abstractmethod
    def pointType(self)->type[DataPoint]: 
        pass 

                               
    @property         
    @abstractmethod
    def inDict(self)->dict[int,DataPoint]: 
        """set containing valid DataPoint. Return an empty
        dict if there is no valid DataPoint"""
        pass 
    
    @property
    def hashSet(self)->set[str]: 
        hSet = set()
        for iHash,iPoint in self.inDict.items():
            hSet.add(iHash)
        return hSet 

    @abstractmethod
    def acceptVistor(
        self,
        v):
        pass

    @abstractmethod
    def acceptOutVistor(
        self,
        v,
        dest:str): 
        """call the corrsponding method in v
        """        
        pass 


    @classmethod
    @abstractmethod
    def convertible(
        cls,
        targetClass:type[Element]
        )->bool:
        pass 
                       
    
    @abstractmethod
    def convertTo(self,targetClass:type[Element])->Element:
        pass 


    
    @classmethod
    @abstractmethod
    def getConveribleClasses(cls)->list[type[Element]]:
        """Return a list of type[Element] that can be 
        converted by this Element class
        """        
        pass 
        

    
    
