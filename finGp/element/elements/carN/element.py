from __future__ import annotations

from ...._date_utils import DateRepresentation
from ...base import DataPoint,Element
from .accept import CarNVisitorHandler

class CarNDataPoint(DataPoint):     
    def __init__(
        self,
        previousDate:DateRepresentation|str,
        followingDate:DateRepresentation|str,
        date:DateRepresentation|str=None,
        cumulativeAbnormalReturn:float=None,
        intervalN:int=None): 

        self._date = DateRepresentation(date)
        self._previousDate = DateRepresentation(previousDate)
        self._followingDate = DateRepresentation(followingDate)
        try:
            self._cumulativeAbnormalReturn = float(cumulativeAbnormalReturn)
        except: 
            self._cumulativeAbnormalReturn = None 
        self._intervalN = intervalN


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
        validE = (isinstance(self._intervalN,int) 
                    and self._intervalN > 2 
                    and self._intervalN % 2 == 1)
        if validA and validB and validC and validD and validE:
            return  True
        else:
            return False

    
    @classmethod
    def correspondingGroupElement(cls)->type[CarNElement]:
        return CarNElement       

    @classmethod
    def getGroupElement(cls, points:list[CarNDataPoint]):
        return CarNElement(points)



class CarNElement(Element):         
    def __init__(self,points:list[CarNDataPoint]=None,interval=3):            
        if points is None:
            points = []              
        self._dataPoints = []
        self.dataPoints = points   # This will validate and set self._items  
        
        
        self.interval = interval
        

    @property
    def dataPoints(self)->list[CarNDataPoint]: 
        return self._dataPoints

    @dataPoints.setter
    def dataPoints(self,points):
        validPoints = []
        for iPoint in points:
            if isinstance(iPoint,CarNDataPoint) and iPoint.valid():                
                validPoints.append(iPoint)
        self._dataPoints = validPoints
        
  
    @property
    def visitorHandler(self)->CarNVisitorHandler:
        return CarNVisitorHandler(self)    
    
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
    def pointType(cls)->type[CarNDataPoint]:
        return CarNDataPoint


    