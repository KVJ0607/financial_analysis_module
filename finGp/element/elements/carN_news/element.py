from __future__ import annotations

from ...._date_utils import DateRepresentation
from ... import DataPoint,Element
from ...elements.carN.element  import CarNDataPoint
from ...elements.noneElement import NoneDataPoint

from .accept import CarNewsVisitorHandler
    
class CarNewsDataPoint(DataPoint):
    def __init__(self,carN:CarNDataPoint,accumlatedSentimentalScore:float=None):
        if isinstance(carN,CarNDataPoint):
            self.carN = carN
        else:
            self.carN = NoneDataPoint()
        try:                
            self.accumlatedSentimentalScore = float(accumlatedSentimentalScore)
        except: 
            self.accumlatedSentimentalScore = None
        
    def __hash__(self): 
        return hash(self.carN)
    
    @property
    def date(self)->DateRepresentation:
        return self.carN.date
    
    def valid(self)->bool:  
        return (DateRepresentation.isValidDateObj(self.date)
                and isinstance(self.accumlatedSentimentalScore,float))        

    @classmethod
    def correspondingGroupElement(cls)->type[CarNewsElement]:
        return CarNewsElement  
        
    @classmethod
    def getGroupElement(
        cls,
        points:list[CarNewsDataPoint])->CarNewsElement: 
        return  CarNewsElement(points)
     
               
    
class CarNewsElement(Element):
    
    def __init__(self,points:list[CarNewsDataPoint]=[]):
        self.dataPoints = points 
        
    
    @property
    def dataPoints(self)->list[CarNewsDataPoint]: 
        return self._dataPoint
    
    @dataPoints.setter
    def dataPoints(self,val:list[CarNewsDataPoint]): 
        validPoints = []
        for iPoint in val: 
            if iPoint.valid() and isinstance(iPoint,CarNewsDataPoint):
                validPoints.append(iPoint)
        self._dataPoint = validPoints            

    @property
    def visitorHandler(self)->CarNewsVisitorHandler:
        return CarNewsVisitorHandler(self)

    @classmethod
    def pointType(cls)->type[CarNewsDataPoint]:
        return CarNewsDataPoint
                    