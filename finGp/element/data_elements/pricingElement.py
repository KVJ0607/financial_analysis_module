from __future__ import annotations

from ...date_utils import DateRepresentation
from ..base import DataPointBase, ElementBase
from ..setopsMixin import SetOpsMixin
from ..conversionMixin import ConversionMixin
from .carNElement import CarNElement, CarNDataPoint
from ..visitorMixin import VisitorMixin
    
class PricingDataPoint(DataPointBase): 
    def __init__(self,date,open,high,low,close,adjClose,volume):               
        self.date = date
        self.__open = open 
        self.__high = high 
        self.__low = low
        self.__close = close 
        self.__adjClose = adjClose
        self.__volume = volume
            
 
    def __hash__(self): return int("12" + str(self.date).replace('-', ''))
    
    @property
    def date(self): return self.__date
    
    @date.setter
    def date(self, val): self.__date = DateRepresentation(val) if val else None

    @property
    def correspondingGroupElement(self): return PricingElement        
    
    @property
    def adjClose(self):
        try:
            return float(self.__adjClose) 
        except: 
            return None
    
    
    def valid(self)->bool:   
        return DateRepresentation.isValid(self.date) and self.adjClose is not None and isinstance(self.adjClose, float)        

    
  
    @classmethod
    def getGroupElement(cls,points:list[DataPointBase]): return PricingElement(points)  
        
    def getTypeGroupElement(cls):return PricingElement
    
    


class PricingConversion(ConversionMixin):     
      
    def convertTo(
        self,
        targetTemplate:ElementBase|type[ElementBase])->ElementBase:
        
        if (type(targetTemplate) == CarNElement
            or issubclass(targetTemplate,CarNElement)):
            return self.__convertToCarNColl(targetTemplate)  
        
        
    def __convertToCarNColl(
        self,
        targetTemplate:CarNElement|type[CarNElement])->ElementBase|CarNElement: 
        if isinstance(targetTemplate,CarNElement):
            nDay = targetTemplate.interval
        elif issubclass(targetTemplate,CarNElement):
            nDay = 3
        else:
            raise TypeError("Unsupported targetTemplate type for conversion.")
        
        deltaDay = (nDay - 1) // 2  # Ensure nDay is an integer
        
        dateList = [] 
        for iPoint in self.dataPoints: 
            dateList.append(iPoint.date)
            
        dateList.sort()
        datesSet = set(dateList)  
        elementLookUp = dict()
        for iPoint in self.dataPoints:
            elementLookUp[hash(iPoint)] = iPoint
        carNPoints:list = []         
        
        for iDay in DateRepresentation.getDateRange(dateList[1], dateList[-1]):
            
            nextDay = iDay + deltaDay
            lastDay = iDay - deltaDay
            if nextDay in datesSet and lastDay in datesSet:
                nextDayHash = int("12" + str(nextDay).replace('-', ''))
                lastDayHash = int("12" + str(lastDay).replace('-', ''))
                
                nextPoint:PricingDataPoint = elementLookUp[nextDayHash]
                lastPoint:PricingDataPoint = elementLookUp[lastDayHash]
                                
                if lastPoint.valid() and nextPoint.valid():
                    carNPoints.append(CarNDataPoint(
                        iDay,
                        lastDay,
                        nextDay,
                        (nextPoint.adjClose - lastPoint.adjClose) / lastPoint.adjClose,
                        nDay)
                    )
        return CarNElement(carNPoints)


    @classmethod
    def convertible(cls,targetClass:type[ElementBase])->bool:
        return targetClass == CarNElement      

    @classmethod
    def getConvertibleClasses(cls)->list[type[ElementBase]]:
        return [CarNElement]             
    
class PricingVisitor(VisitorMixin):
    def acceptVisitor(self,v):
        return v.visitPricingElement(self)    

    def acceptOutVisitor(
        self,
        v,
        dest:str): 
        return v.visitOutPricingElement(self,dest)
    
    
    
    


class PricingElement(ElementBase,SetOpsMixin,PricingConversion,PricingVisitor):
    def __init__(self,points:list[PricingDataPoint]=None):
        if points is None: points = []
        self._dataPoints = []
        self.dataPoints = points
        
    @property    
    def pointType(self): return PricingDataPoint                             

    @property
    def dataPoints(self):return self._dataPoints
    
    @dataPoints.setter
    def dataPoints(self, points):
        validPoints = []
        for iPoint in points:
            if isinstance(iPoint, PricingDataPoint) and iPoint.valid():
                validPoints.append(iPoint)
        self._dataPoints = validPoints

    

