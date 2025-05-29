   
from __future__ import annotations

from ..operator import Operator
from ...element import Car3Element,Car3DataPoint,PricingElement,PricingDataPoint
from ..._date_utils import DateRepresentation

class PricingSquareOperator(Operator): 

    @classmethod
    def getProductClass(cls)->type[Car3Element]:
        return Car3Element         
                        
            
        
    
    @classmethod
    def getOperands(cls)->set: 
        return set([PricingElement])
        
    
    
    @classmethod
    def dot(
        cls,
        gEleA:PricingElement) -> Car3Element:                        

                
        if not type(gEleA) == PricingElement:
            raise TypeError(f"""{gEleA} are of type {type[gEleA]} but not 
                            {PricingElement}""")

        deltaDay = 1  
        
        dateList = [] 
        for iPoint in gEleA.dataPoints: 
            dateList.append(iPoint.date)            
        dateList.sort()        
        
        datesSet = set(dateList)  
        
        elementLookUp:dict[int,PricingDataPoint] = dict()
        for iPoint in gEleA.dataPoints:
            elementLookUp[hash(iPoint)] = iPoint
            
        carNPoints:list = []                 
        for iDay in DateRepresentation.getDateRange(dateList[1], dateList[-1]):
            
            nextDay = iDay + deltaDay
            lastDay = iDay - deltaDay
            if nextDay in datesSet and lastDay in datesSet:
                nextDayHash = PricingDataPoint.hashFromDate(nextDay)
                lastDayHash = PricingDataPoint.hashFromDate(lastDay)                                                
                nextPoint= elementLookUp[nextDayHash]
                lastPoint = elementLookUp[lastDayHash]
                                
                if lastPoint.valid() and nextPoint.valid():
                    carNPoints.append(Car3DataPoint(                        
                        lastDay,
                        nextDay,
                        iDay,
                        (nextPoint.adjClose - lastPoint.adjClose) / lastPoint.adjClose,
                        3)
                    )
        return Car3Element(carNPoints) 
        
           


        
           
