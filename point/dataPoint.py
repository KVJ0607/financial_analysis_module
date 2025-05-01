from abc import ABC,abstractmethod

from date_utils.dateRepresentation import DateRepresentation


class DataPoint(ABC):        

    def __str__(self): 
        pass 

    @property
    @abstractmethod
    def date(self)->DateRepresentation:
        pass
        
    # @property
    # @abstractmethod
    # def coordinate(self)->str:
    #     '''
    #     It is like indexing on some attributes of an object. 
    #     Every data point has a coordinate. DataPoint with the same coordinate is considered to be comparable
    #     e.g. Pricing history of the same date has the same coordinate regardless other attribute
    #     '''
    #     pass 
    
                
    @abstractmethod
    def valid(self)->bool:  
        '''Return true if it is a valid data. The implementation logic based on the actual subclass'''
        pass 
    
    # @classmethod
    # @abstractmethod
    # def getCoordinateFrom(cls)->str: 
    #     pass 
    
    @classmethod    
    @abstractmethod
    def equivalent(cls,*arg)->bool: 
        '''Return if they have the same coordinate'''
        pass 
    

    @classmethod
    @abstractmethod
    def getGroupElement(cls,points:list['DataPoint'])->'GroupElement': 
        pass 

class GroupElement(ABC): 
    @property
    @abstractmethod
    def eleClass(self)->type[DataPoint]: 
        pass  
         
    @abstractmethod
    def element(self)->list[DataPoint]: 
        pass 
