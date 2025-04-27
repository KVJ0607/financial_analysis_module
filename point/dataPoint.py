from abc import ABC,abstractmethod

from date_utils.dateRepresentation import DateRepresentation


class DataPoint(ABC):        

    def __str__(self): 
        return str(self.mapping)

    @property
    @abstractmethod
    def date(self)->DateRepresentation:
        pass
    
    @property                
    @abstractmethod
    def mapping(self)->map:    
        '''Return a map[attribute,data figures]'''     
        pass 
    
    
    @abstractmethod
    def getDataValueWithAttribute(self,attribute:str): 
        pass 
    
    @property
    @abstractmethod
    def coordinate(self)->str:
        '''
        It is like indexing on some attributes of an object. 
        Every data point has a coordinate. DataPoint with the same coordinate is considered to be comparable
        e.g. Pricing history of the same date has the same coordinate regardless other attribute
        '''
        pass 
    
            
    @abstractmethod
    def valid(self)->bool:  
        '''Return true if it is a valid data. The implementation logic based on the actual subclass'''
        pass 
    
    @classmethod
    @abstractmethod
    def getCoordinateFrom(cls)->str: 
        pass 
    
    @classmethod    
    @abstractmethod
    def comparable(cls,*arg)->bool: 
        '''Return if they have the same coordinate'''
        pass 
    
    
    @staticmethod
    def verifyAndGetValidListOfDataPoint(listOfEvents:list['DataPoint']):
        goodList=[]
        if not isinstance(listOfEvents,list): 
            listOfEvents = list(listOfEvents)
        for event in listOfEvents: 
            if not isinstance(listOfEvents,DataPoint): 
                print('Warning: ', event,' is not a DataPoint.') 
            goodList.append(event)
        return event

    


         
