from __future__ import annotations

from ...._date_utils import DateRepresentation
from ... import DataPoint,Element
from ...elements.car3.element  import Car3DataPoint
from ...elements.noneElement import NoneDataPoint

from .accept import CarNewsVisitorHandler
    
class Car3NewsDataPoint(DataPoint):
    def __init__(self,carN:Car3DataPoint,accumlatedSentimentalScore:float=None):
        if isinstance(carN,Car3DataPoint):
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
    def correspondingGroupElement(cls)->type[Car3NewsElement]:
        return Car3NewsElement  
        
    @classmethod
    def getGroupElement(
        cls,
        points:list[Car3NewsDataPoint])->Car3NewsElement: 
        return  Car3NewsElement(points)
     
               
    
class Car3NewsElement(Element):
    
    def __init__(self,points:list[Car3NewsDataPoint]=[]):
        self.dataPoints = points 
        
    
    @property
    def dataPoints(self)->list[Car3NewsDataPoint]: 
        return self._dataPoint
    
    @dataPoints.setter
    def dataPoints(self,val:list[Car3NewsDataPoint]): 
        validPoints = []
        for iPoint in val: 
            if iPoint.valid() and isinstance(iPoint,Car3NewsDataPoint):
                validPoints.append(iPoint)
        self._dataPoint = validPoints            

    
    def getVisitorHandler(self)->CarNewsVisitorHandler:
        return CarNewsVisitorHandler(self)

    @classmethod
    def pointType(cls)->type[Car3NewsDataPoint]:
        return Car3NewsDataPoint
                    