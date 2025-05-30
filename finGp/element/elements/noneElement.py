from __future__ import annotations


from ..._date_utils import DateRepresentation
from ..base import DataPoint,Element

        
class NoneDataPoint(DataPoint): 
    '''
    A special class that represent the absent of market day 
    '''
    def __init__(self,date = None):
        self._date = DateRepresentation.getNullInstance() if date is None else DateRepresentation(date)

    def __hash__(self): return int("10" + str(self.date).replace('-', ''))      
    
    def __bool__(self): return False  


    @property
    def date(self): return self._date     

    
    def valid(self)->bool: 
        return False                             
    
  
    @classmethod
    def correspondingGroupElement(cls)->type[NoneElement]:
        return NoneElement  
    
    @classmethod
    def getGroupElement(cls): return NoneElement()




    

class NoneElement(Element):    
    def __init__(self): self._items = []      
    
    def __bool__(self): return False

    @property
    def dataPoints(self): return self._items
    
    @dataPoints.setter
    def dataPoints(self, points): self._items = []

    

    
    @classmethod
    def getPointType(cls)->type[NoneDataPoint]:
        return NoneDataPoint