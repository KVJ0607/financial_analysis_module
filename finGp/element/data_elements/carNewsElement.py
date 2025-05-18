from __future__ import annotations

from ...date_utils import DateRepresentation
from .. import DataPointBase,ElementBase,CarNDataPoint,NoneDataPoint
from ..setopsMixin import SetOpsMixin
from ..visitorMixin import VisitorMixin
    
class CarNewsDataPoint(DataPointBase):
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

class CarNewsVisitor(VisitorMixin): 
    def acceptVisitor(self,v):
        return v.visitCarsNewsElement(self)  

   
    def acceptOutVisitor(
        self,
        v,
        dest:str): 
        return v.visitOutCarsNewsElement(self,dest)        
               
    
class CarNewsElement(ElementBase,SetOpsMixin,CarNewsVisitor):
    
    def __init__(self,points:list[CarNewsDataPoint]=[]):
        self.dataPoints = points 
        
    @property
    def pointType(self)->type[DataPointBase]: return CarNewsDataPoint
    
    @property
    def dataPoints(self): return self._dataPoint
    
    @dataPoints.setter
    def dataPoints(self,val:list[CarNewsDataPoint]): 
        validPoints = []
        for iPoint in val: 
            if iPoint.valid() and isinstance(iPoint,CarNewsDataPoint):
                validPoints.append(iPoint)
        self._dataPoint = validPoints            




    
        
                 