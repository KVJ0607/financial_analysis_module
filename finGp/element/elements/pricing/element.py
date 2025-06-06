from __future__ import annotations


from ...._date_utils import DateRepresentation

from ...base import DataPoint, Element


 

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
    
    @classmethod
    def hashFromDate(cls, date:DateRepresentation|str)->int:
        return int("12" + str(date).replace('-', '')) if date else None
    
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

    def toJson(self):
        return {
            "id": self.__hash__(),
            "type_name": self.__class__.__name__,
            "date": str(self.date),
            "open": self._open,
            "high": self._high,
            "low": self._low,
            "close": self._close,
            "adjClose": self._adjClose,
            "volume": self._volume
        }
    
    @classmethod
    def correspondingGroupElement(cls)->type[PricingElement]:
        return PricingElement      
    
    @classmethod
    def getGroupElement(cls,points:list[PricingDataPoint])->PricingElement: 
        return PricingElement(points)

        
    
    

    
    


class PricingElement(Element):    
    
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
    

    
    @classmethod    
    def getPointType(cls)->type[PricingDataPoint]:
        return PricingDataPoint      
    
