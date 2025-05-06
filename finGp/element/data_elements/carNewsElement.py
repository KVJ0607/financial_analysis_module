from __future__ import annotations

from ...date_utils import DateRepresentation
from .. import DataPoint,Element,CarNDataPoint,NoneDataPoint

    
class CarNewsDataPoint(DataPoint):
    def __init__(self,carN,accumlatedSentimentalScore:float):
        if isinstance(carN,CarNDataPoint):
            self.carN = carN
        else:
            self.carN = NoneDataPoint
        try:                
            self.accumlatedSentimentalScore = float(accumlatedSentimentalScore)
        except: 
            self.accumlatedSentimentalScore = None
        
    def __hash__(self): 
        return self.carN.__hash__()
    
    @property
    def date(self)->DateRepresentation:
        return self.carN.date
    
    def valid(self)->bool:  
        return (self.date.isValid() 
                and isinstance(self.accumlatedSentimentalScore,float))        
    
    @classmethod
    def getGroupElement(
        cls,
        points:list[CarNewsDataPoint])->CarNewsElement: 
        return  CarNewsElement(points)


    
class CarNewsElement(Element):
    
    def __init__(self,points:list[CarNewsDataPoint]):
        self.inDict = points 
        
    @property
    def pointType(self)->type[DataPoint]: 
        return CarNewsDataPoint
    
    @property
    def inDict(self)->dict[str,CarNewsDataPoint]:
        return self.__element
    
    @inDict.setter
    def inDict(self,val:list[CarNewsDataPoint]): 
        validPoints = dict()
        for iPoint in val: 
            if iPoint.valid() and isinstance(iPoint,CarNewsDataPoint):
                validPoints[iPoint.__hash__()] = iPoint
        self.__element = validPoints            


    def acceptVistor(self,v):
        return v.visitCarsNewsElement(self)  

   
    def acceptOutVistor(
        self,
        v,
        dest:str): 
        return v.visitOutCarsNewsElement(self,dest)        
        

    @classmethod
    def convertible(cls,targetClass:type[Element])->bool:
        return False 
    
    def convertTo(self,targetClass:type[Element])->'Element':
        pass     
         
    @classmethod
    def getConveribleClasses(cls)->list[type[DataPoint]]:
        return []    
            

        
        
                 