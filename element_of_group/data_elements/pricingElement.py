from __future__ import annotations

from date_utils import DateRepresentation
from ..element import DataPoint,Element
from .carNElement import CarNDataPoint,CarNElement
from .NoneElement import NoneDataPoint
from collection_vistor import Vistor
    
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
    def date(self,val):
        self.__date = DateRepresentation(val)

    @property
    def correspondingGroupElement(self)->Element:
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
    def getGroupElement(cls,points:list[DataPoint])->Element: 
        return PricingElement(points)  
        
    def getTypeGroupElement(cls)->type[Element]:
        return PricingElement
    
    

class PricingElement(Element):
    def __init__(self,points:list[PricingDataPoint]):
        self.inList = points 
    
    @property    
    def pointType(self)->type[DataPoint]: 
        return PricingDataPoint  
         
    @property
    def inList(self)->dict[int,PricingDataPoint]: 
        return self.__element
    
    @inList.setter
    def inList(self,val:list[DataPoint]):
        validPoints = dict()
        for iPoint in val: 
            if isinstance(iPoint,PricingDataPoint):
                if iPoint.valid():
                    validPoints[iPoint.__hash__()]=(iPoint)
        self.__element = validPoints                     

    
    @property
    def dates(self)->list[DateRepresentation]:
        thisDates = []
        for iEle in self.inList.values(): 
            thisDates.append(iEle.date)
        return thisDates


    def acceptVistor(self,v:Vistor):
        return v.visitPricingElement(self)    

    def acceptOutVistor(
        self,
        v:Vistor,
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
        nDay = (nDay-1)/2             
        
        dateList = sorted(self.dates)
        
        carNPoints:list = [] 
        for iDay in DateRepresentation.getDateRange(dateList[1],dateList[-1]):
            if iDay+nDay in dateList and iDay-nDay in dateList:
                lastPoint:PricingDataPoint = self.getPointFrom(iDay-nDay)
                nextPoint:PricingDataPoint = self.getPointFrom(iDay+nDay)
                if lastPoint.valid() and nextPoint.valid():
                    carNPoints.append(CarNDataPoint(
                        iDay,
                        iDay-nDay,
                        iDay+nDay,
                        (nextPoint.adjClose-lastPoint.adjClose)/lastPoint.adjClose,
                        nDay)
                    )
        return CarNElement(carNPoints)

    
    def getPointFrom(self,date:DateRepresentation)->PricingDataPoint:
        hashStr = ("12"+str(date).replace('-',''))        
        return self.inList.get(int(hashStr),NoneDataPoint)    
    

    @classmethod
    def getConveribleClasses(cls)->list[type[Element]]:
        return [CarNElement]    