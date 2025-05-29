from __future__ import annotations

from ...._date_utils import DateRepresentation
from ...base import DataPoint,Element
from .accept import Car3VisitorHandler

class Car3DataPoint(DataPoint):     
    def __init__(
        self,
        previousDate:DateRepresentation|str,
        followingDate:DateRepresentation|str,
        date:DateRepresentation|str=None,
        cumulativeAbnormalReturn:float=None): 

        self._date = DateRepresentation(date)
        self._previousDate = DateRepresentation(previousDate)
        self._followingDate = DateRepresentation(followingDate)
        try:
            self._cumulativeAbnormalReturn = float(cumulativeAbnormalReturn)
        except: 
            self._cumulativeAbnormalReturn = None 
        self._intervalN = 3


    def __hash__(self): 
        hashStr = ("13" 
                    +str(self.previousDate).replace('-','')
                    +str(self.followingDate).replace('-','')
                    +str(self._intervalN))
        return int(hashStr)
        
    @property
    def date(self)->DateRepresentation:
        return self._date 
                
    @property
    def previousDate(self)->DateRepresentation:
        return self._previousDate    
        
    @property
    def followingDate(self)->DateRepresentation: 
        return self._followingDate        
    
    @property
    def cumulativeAbnormalReturn(self)->float: 
        return self._cumulativeAbnormalReturn

    @property
    def intervalN(self)->int: 
        return self._intervalN        
         
        
    def valid(self)->bool:  
        
        validA = DateRepresentation.isValidDateObj(self._date)
        validB = DateRepresentation.isValidDateObj(self._previousDate)
        validC = DateRepresentation.isValidDateObj(self._followingDate)
        validD = self._cumulativeAbnormalReturn is not None and isinstance(self._cumulativeAbnormalReturn, (int, float))
        if validA and validB and validC and validD:
            return  True
        else:
            return False

    
    @classmethod
    def correspondingGroupElement(cls)->type[Car3Element]:
        return Car3Element       

    @classmethod
    def getGroupElement(cls, points:list[Car3DataPoint]):
        return Car3Element(points)



class Car3Element(Element):         
    def __init__(self,points:list[Car3DataPoint]=None):            
        if points is None:
            points = []              
        self._dataPoints = []
        self.dataPoints = points   # This will validate and set self._items  
        
        
        self.interval = 3
        

    @property
    def dataPoints(self)->list[Car3DataPoint]: 
        return self._dataPoints

    @dataPoints.setter
    def dataPoints(self,points):
        validPoints = []
        for iPoint in points:
            if isinstance(iPoint,Car3DataPoint) and iPoint.valid():                
                validPoints.append(iPoint)
        self._dataPoints = validPoints
        
  
    
    def getVisitorHandler(self)->Car3VisitorHandler:
        return Car3VisitorHandler(self)    
    
    @property
    def interval(self)->int:
        return self._interval    
    
    @interval.setter
    def interval(self,nDay:int): 
        if nDay%2 == 0: 
            raise ValueError("nDay should be an odd number")
        if nDay < 1: 
            raise ValueError("nDay should be a positive number")
        self._interval = nDay   

    @classmethod
    def pointType(cls)->type[Car3DataPoint]:
        return Car3DataPoint


    