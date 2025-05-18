from __future__ import annotations


from ...date_utils import DateRepresentation
from ..base import DataPointBase,ElementBase

        
class NoneDataPoint(DataPointBase): 
    '''
    A special class that represent the absent of market day 
    '''
    def __init__(self,date = None):
        self.__date = DateRepresentation.getNullInstance() if date is None else DateRepresentation(date)

    def __hash__(self): return int("10" + str(self.date).replace('-', ''))        


    @property
    def date(self): return self.__date
  
    @property
    def correspondingGroupElement(self): return NoneElement       

    
    def valid(self): return False                             
    
    
    @classmethod
    def getGroupElement(cls): return NoneElement()

    @classmethod
    def getTypeGroupElement(cls): return NoneElement


class NoneElement(ElementBase):    
    def __init__(self): self._items = []      
    
    @property
    def pointType(self): return NoneDataPoint

    @property
    def dataPoints(self): return self._items
    
    @dataPoints.setter
    def dataPoints(self, points): self._items = []

    