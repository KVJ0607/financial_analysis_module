from ...._date_utils import DateRepresentation

from ...base import Element
from ..._helpers.conversion import Conversion

from typing import TypeVar
T = TypeVar("T", bound="Element")

class PricingConversion(Conversion):     
    from ..carN.element import CarNElement, CarNDataPoint    

        
    def convertTo(
        self,
        targetTemplate:Element|type[T])->T:
        
        if (type(targetTemplate) == self.CarNElement
            or issubclass(targetTemplate,self.CarNElement)):
            return self._convertToCarNColl(targetTemplate)  

    @classmethod
    def convertible(cls,targetClass:type[Element])->bool:
        return targetClass == cls.CarNElement      

    @classmethod
    def getConvertibleClasses(cls)->list[type[Element]]:
        return [cls.CarNElement]             
    
    def _convertToCarNColl(
        self,
        targetTemplate:CarNElement|type[CarNElement])->CarNElement: 
        if isinstance(targetTemplate,self.CarNElement):
            nDay = targetTemplate.interval
        elif issubclass(targetTemplate,self.CarNElement):
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
                
                nextPoint= elementLookUp[nextDayHash]
                lastPoint = elementLookUp[lastDayHash]
                                
                if lastPoint.valid() and nextPoint.valid():
                    carNPoints.append(self.CarNDataPoint(                        
                        lastDay,
                        nextDay,
                        iDay,
                        (nextPoint.adjClose - lastPoint.adjClose) / lastPoint.adjClose,
                        nDay)
                    )
        return self.CarNElement(carNPoints)    

