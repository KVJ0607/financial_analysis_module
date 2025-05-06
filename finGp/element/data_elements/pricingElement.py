from __future__ import annotations

from typing import Iterator

from ...date_utils import DateRepresentation
from ..element import DataPoint,Element
from .carNElement import CarNDataPoint,CarNElement
from .NoneElement import NoneDataPoint

    
class PricingDataPoint(DataPoint): 
    def __init__(self,date,open,high,low,close,adjClose,volume):               
        self.date = date
        self.__open = open 
        self.__high = high 
        self.__low = low
        self.__close = close 
        self.__adjClose = adjClose
        self.__volume = volume
            
        
    

    def __hash__(self): 
        hashStr = ("12"+str(self.date).replace('-',''))
        return int(hashStr)
 

    @property
    def date(self)->DateRepresentation:
        return self.__date
    
    @date.setter
    def date(self, val):
        self.__date = DateRepresentation(val) if val else None

    @property
    def correspondingGroupElement(self)->type[Element]:
        return PricingElement        
    
    @property
    def adjClose(self)->float:
        try:
            return float(self.__adjClose) 
        except: 
            return None
    
    
    def valid(self)->bool:   
        if not DateRepresentation.isValid(self.date): 
            return False
                
        if (self.adjClose is None) or (not isinstance(self.adjClose,float)): 
            return False
        
        return True
    
  
    @classmethod
    def getGroupElement(cls,points:list[DataPoint])->PricingElement: 
        return PricingElement(points)  
        
    def getTypeGroupElement(cls)->type[Element]:
        return PricingElement
    
    

class PricingElement(Element):
    def __init__(self,points:list[PricingDataPoint]):
        self.inDict = points 
    
    @property    
    def pointType(self)->type[DataPoint]: 
        return PricingDataPoint  
         
    @property
    def inDict(self)->dict[int,PricingDataPoint]: 
        return self.__element
    
    @inDict.setter
    def inDict(self,val:list[DataPoint]):
        validPoints = dict()
        for iPoint in val: 
            if isinstance(iPoint,PricingDataPoint):
                if iPoint.valid():
                    validPoints[iPoint.__hash__()]= iPoint
        self.__element = validPoints                     

    
    
    @property
    def dates(self) -> Iterator[DateRepresentation]:
        return (iEle.date for iEle in self.inDict.values())
    

    def acceptVistor(self,v):
        return v.visitPricingElement(self)    

    def acceptOutVistor(
        self,
        v,
        dest:str): 
        return v.visitOutPricingElement(self,dest)
    
    
    @classmethod
    def convertible(cls,targetClass:type[Element])->bool:
        if targetClass == CarNElement:
            return True
        else: 
            return False
    
    
    def convertTo(self,targetClass:type[Element])->Element:
        if targetClass == CarNElement:
            return self.__convertToCarNColl()  
        
        
    def __convertToCarNColl(self,nDay:int=3)->Element|CarNElement: 
        if nDay//2 == 0: 
            raise ValueError("nDay should be an odd number")
        if nDay < 1: 
            raise ValueError("nDay should be a positive number")
        deltaDay = (nDay - 1) // 2  # Ensure nDay is an integer
        
        dateList = sorted(self.dates)
        datesSet = set(dateList)  
        carNPoints:list = [] 
        
        for iDay in DateRepresentation.getDateRange(dateList[1], dateList[-1]):
            
            nextDay = iDay + deltaDay
            lastDay = iDay - deltaDay
            if nextDay in datesSet and lastDay in datesSet:
                nextPoint:PricingDataPoint = self.getPointFrom(nextDay)
                lastPoint:PricingDataPoint = self.getPointFrom(lastDay)
                if lastPoint.valid() and nextPoint.valid():
                    carNPoints.append(CarNDataPoint(
                        iDay,
                        lastDay,
                        nextDay,
                        (nextPoint.adjClose - lastPoint.adjClose) / lastPoint.adjClose,
                        nDay)
                    )
        print("Number of points: ", len(carNPoints))
        return CarNElement(carNPoints)

    
    def getPointFrom(self,date:DateRepresentation)->PricingDataPoint:
        hashStr = ("12"+str(date).replace('-',''))        
        return self.inDict.get(int(hashStr),NoneDataPoint)    
    

    @classmethod
    def getConveribleClasses(cls)->list[type[Element]]:
        return [CarNElement]    