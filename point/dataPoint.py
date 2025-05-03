from __future__ import annotations
from abc import ABC,abstractmethod
from typing import Callable

from date_utils.dateRepresentation import DateRepresentation


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
    def correspondingGroupElement(self)->GroupElement:
        pass        
    
                
    @abstractmethod
    def valid(self)->bool:  
        '''Return true if it is a valid data. The implementation logic based on the actual subclass'''
        pass 
    

    @classmethod
    @abstractmethod
    def getGroupElement(cls,points:list['DataPoint'])->GroupElement: 
        pass 
    
    @classmethod
    @abstractmethod
    def getTypeGroupElement(cls)->type[GroupElement]:
        pass 

class GroupElement(ABC): 
    @property
    @abstractmethod
    def eleClass(self)->type[DataPoint]: 
        pass 

    @property
    def eleClassInStr(self)->str: 
        return self.eleClass.__name__
                           
    @property         
    @abstractmethod
    def element(self)->dict[int,DataPoint]: 
        """set containing valid DataPoint. Return an empty
        set if there is no valid DataPoint"""
        pass 
    
    @abstractmethod
    def convertible(self,targetClass:type[DataPoint])->bool:
        pass 
    
    @abstractmethod
    def convertTo(self,targetClass:type[DataPoint])->'GroupElement':
        pass 
    
    
    @classmethod
    def pointwise(cls,eleA:GroupElement,eleB:GroupElement,opperation):
        if eleA.eleClass != eleB.eleClass: 
            raise TypeError(f"""{eleA} and {eleB} are of type {type(eleA)}
                            and {type(eleB)}. They should be of 
                            the same type""")
        
        if not callable(opperation): 
            raise AttributeError(f"{opperation} is not callable")
        
        for iHashA,iPointA in eleA.element.items():
            if iPointA in eleB.element:
                newPoint = opperation(
                    iPointA,
                    eleB.element[iHashA]
                )
                
                eleA.element[iHashA] = newPoint
                eleB.element[iHashA] = newPoint

