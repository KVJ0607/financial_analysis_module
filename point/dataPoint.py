from __future__ import annotations
from abc import ABC,abstractmethod


from typing import Callable

from date_utils.dateRepresentation import DateRepresentation
from collection_vistor import Vistor

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
    def correspondingGroupElement(self)->Element:
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
    def type(self)->type[DataPoint]: 
        pass 

    @property
    def type_InStr(self)->str: 
        return self.type.__name__
    
                               
    @property         
    @abstractmethod
    def inList(self)->dict[int,DataPoint]: 
        """set containing valid DataPoint. Return an empty
        set if there is no valid DataPoint"""
        pass 


    @abstractmethod
    def acceptVistor(
        self,
        v:Vistor):
        pass

    @abstractmethod
    def acceptOutVistor(
        self,
        v:Vistor,
        dest:str): 
        pass 

    @classmethod
    @abstractmethod
    def convertible(
        cls,
        targetClass:type[DataPoint]
        )->bool:
        pass 
    
    
                    
    
    @abstractmethod
    def convertTo(self,targetClass:type[DataPoint])->'Element':
        pass 


    
    @classmethod
    @abstractmethod
    def getConvertResultClasses(cls)->list[DataPoint]:
        pass 
        

    
    
