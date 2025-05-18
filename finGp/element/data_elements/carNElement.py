from __future__ import annotations

from ...date_utils import DateRepresentation
from ..base import DataPointBase,ElementBase
from ..setopsMixin import SetOpsMixin
from ..visitorMixin import VisitorMixin

class CarNDataPoint(DataPointBase):     
    def __init__(self,date,previousDate,followingDate,cumulativeAbnormalReturn,intervalN): 

        self.__date = DateRepresentation(date)
        self.__previousDate = DateRepresentation(previousDate)
        self.__followingDate = DateRepresentation(followingDate)
        try:
            self.__cumulativeAbnormalReturn = float(cumulativeAbnormalReturn)
        except: 
            self.__cumulativeAbnormalReturn = None 
        self.__intervalN = intervalN


    def __hash__(self): 
        hashStr = ("13" 
                    +str(self.previousDate).replace('-','')
                    +str(self.followingDate).replace('-','')
                    +str(self.__intervalN))
        return int(hashStr)
        
    @property
    def date(self)->DateRepresentation:
        return self.__date

    @property
    def correspondingGroupElement(self)->type[ElementBase]:
        return CarNElement        
                
    @property
    def previousDate(self)->DateRepresentation:
        return self.__previousDate    
        
    @property
    def followingDate(self)->DateRepresentation: 
        return self.__followingDate        
    
    @property
    def cumulativeAbnormalReturn(self)->float: 
        return self.__cumulativeAbnormalReturn

    @property
    def intervalN(self)->int: 
        return self.__intervalN        
         
        
    def valid(self)->bool:  
        
        validA = DateRepresentation.isValid(self.__date)
        validB = DateRepresentation.isValid(self.__previousDate)
        validC = DateRepresentation.isValid(self.__followingDate)
        validD = self.__cumulativeAbnormalReturn is not None and isinstance(self.__cumulativeAbnormalReturn, (int, float))
        validE = (isinstance(self.__intervalN,int) 
                    and self.__intervalN > 2 
                    and self.__intervalN % 2 == 1)
        if validA and validB and validC and validD and validE:
            return  True
        else:
            return False

    


    @classmethod
    def getGroupElement(cls, points:list[CarNDataPoint]):
        return CarNElement(points)

    @classmethod
    def getTypeGroupElement(cls)->type[ElementBase]:
        return CarNElement 

class CarNVisitor(VisitorMixin):
        
    def acceptVisitor(self,v):
        return v.visitCarNElement(self.dataPoints)            

    def acceptOutVisitor(
        self,
        v,
        dest:str): 
        return v.visitOutCarNElement(self.dataPoints,dest)    
            
class CarNElement(ElementBase,SetOpsMixin,CarNVisitor):
            
    def __init__(self,points:list[CarNDataPoint]=None,interval=3):    
        if points is None:
            points = [] 
             
        self._dataPoints = []
        self.dataPoints = points   # This will validate and set self._items  
        self.interval = interval


    @property
    def dataPoints(self): 
        return self._dataPoints

    @dataPoints.setter
    def dataPoints(self,points):
        validPoints = []
        for iPoint in points:
            if isinstance(iPoint,CarNDataPoint) and iPoint.valid():                
                validPoints.append(iPoint)
        self._dataPoints = validPoints
        
    @property
    def pointType(self): return CarNDataPoint
    
    @property
    def interval(self): return self.__interval    
    
    @interval.setter
    def interval(self,nDay:int): 
        if nDay%2 == 0: 
            raise ValueError("nDay should be an odd number")
        if nDay < 1: 
            raise ValueError("nDay should be a positive number")
        self.__interval = nDay 

            


  

    