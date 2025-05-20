from __future__ import annotations


from ...._date_utils import DateRepresentation

from ...base import DataPoint, Element
from ...helper.non_generator.registry import Registry

from .conversion import PricingConversion
from .accept import PricingVisitorHandler

class PricingDataPoint(DataPoint): 
    def __init__(
        self,
        date:DateRepresentation|str,
        open:str|float=None,
        high:str|float=None,
        low:str|float=None,
        close:str|float=None,
        adjClose:str|float=None,
        volume:str|float=None):   
                    
        self.date = date
        self._open = open 
        self._high = high 
        self._low = low
        self._close = close 
        self._adjClose = adjClose
        self._volume = volume
            
 
    def __hash__(self): return int("12" + str(self.date).replace('-', ''))
    
    @property
    def date(self)->DateRepresentation:
        return self._date
    
    @date.setter
    def date(self, val): self._date = DateRepresentation(val) if val else None
      
    
    @property
    def adjClose(self)->float:
        try:
            return float(self._adjClose) 
        except: 
            return None
    
    
    def valid(self)->bool:   
        return DateRepresentation.isValidDateObj(self.date) and self.adjClose is not None and isinstance(self.adjClose, float)        

    @classmethod
    def correspondingGroupElement(cls)->type[PricingElement]:
        return PricingElement      
    
    @classmethod
    def getGroupElement(cls,points:list[PricingDataPoint])->PricingElement: 
        return PricingElement(points)

        
    
    

    
    


class PricingElement(Element,PricingConversion):    
    
    def __init__(self,points:list[PricingDataPoint]=None):
        if points is None: points = []
        self._dataPoints = []
        self.dataPoints = points                                   

    @property
    def dataPoints(self)->list[PricingDataPoint]:
        return self._dataPoints
    
    @dataPoints.setter
    def dataPoints(self, points):
        self._dataPoints = [p for p in points if isinstance(p, PricingDataPoint) and p.valid()]    
    
    @property    
    def visitorHandler(self)->PricingVisitorHandler:
        return PricingVisitorHandler(self)
    
    @classmethod    
    def pointType(cls)->type[PricingDataPoint]:
        return PricingDataPoint      
    
eleReq = Registry.makeElementRequirements({PricingElement})
Registry.update(PricingConversion.CarNElement,eleReq)    