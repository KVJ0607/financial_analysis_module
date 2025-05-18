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
    def __init__(self,points:list[PricingDataPoint]=[]):
        self.__inDict = points 
    
    @property    
    def pointType(self)->type[DataPoint]: 
        return PricingDataPoint  
         
    @property
    def __inDict(self)->dict[int,PricingDataPoint]: 
        return self.__element
    
        
    @__inDict.setter
    def __inDict(self,val:list[DataPoint]):
        validPoints = dict()
        for iPoint in val: 
            if isinstance(iPoint,PricingDataPoint):
                if iPoint.valid():
                    validPoints[iPoint.__hash__()]= iPoint
        self.__element = validPoints                     

    @property
    def items(self):
        """
        Returns an iterable view of (key, DataPoint) pairs contained in this Element,
        allowing iteration over all DataPoints.
        """
        return self.__inDict.items()    
    
    @property
    def dates(self) -> Iterator[DateRepresentation]:
        return (iEle.date for iEle in self.__inDict.values())

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
    
    
    def convertTo(
        self,
        targetTemplate:Element|type[Element])->Element:
        
        if (type(targetTemplate) == CarNElement
            or issubclass(targetTemplate,CarNElement)):
            return self.__convertToCarNColl(targetTemplate)  
        
        
    def __convertToCarNColl(
        self,
        targetTemplate:CarNElement|type[CarNElement])->Element|CarNElement: 
        if isinstance(targetTemplate,CarNElement):
            nDay = targetTemplate.interval
        elif issubclass(targetTemplate,CarNElement):
            nDay = 3
        else:
            raise TypeError("Unsupported targetTemplate type for conversion.")
        
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
        return CarNElement(carNPoints)

    
    def getPointFrom(self,date:DateRepresentation)->PricingDataPoint:
        hashStr = ("12"+str(date).replace('-',''))        
        return self.__inDict.get(int(hashStr),NoneDataPoint)    
    

    @classmethod
    def getConveribleClasses(cls)->list[type[Element]]:
        return [CarNElement]    
    

    def intersect(self, other: 'Element') -> 'Element':
        """
        Return a new Element containing only the DataPoints that are present in both
        this Element and the other Element, as determined by their identity or hash.

        Args:
            other (Element): Another Element to intersect with.

        Returns:
            Element: A new Element instance with the intersection of DataPoints.
        """
        # Get the intersection of hash keys
        common_hashes = set(self.__inDict.keys()) & set(other.__inDict.keys())
        # Collect DataPoints from self that have these hashes
        intersected_points = [self.__inDict[h] for h in common_hashes]
        # Create a new Element of the same type with these points
        return type(self)(intersected_points)    

    @classmethod
    def intersectMany(cls, *elements: 'Element') -> list['Element']:
        """
        Return a list of Elements, where each element is the intersection of that element
        with all the others in the provided arguments.

        Args:
            *elements (Element): Two or more Element instances to intersect.

        Returns:
            list[Element]: A list of Element instances, each intersected with all others.

        Raises:
            ValueError: If fewer than two elements are provided.
        """
        if len(elements) < 2:
            raise ValueError("At least two Element instances are required for intersection.")

        result = []
        for idx, elem in enumerate(elements):
            # Intersect this element with all others
            others = elements[:idx] + elements[idx+1:]
            common_hashes = set(elem.__inDict.keys())
            for other in others:
                common_hashes &= set(other.__inDict.keys())
            intersected_points = [elem.__inDict[h] for h in common_hashes]
            result.append(type(elem)(intersected_points))
        return result    