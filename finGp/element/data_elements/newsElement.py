from __future__ import annotations

from ...date_utils import DateRepresentation
from ..element import DataPoint,Element
from .NoneElement import NoneDataPoint        

class NewsDataPoint(DataPoint): 
    
    
    def __init__(self,date,siteAddress:str,sentimentalScore:int|str|float):   
        self.date = date 
        self.__siteAddress = siteAddress
        self.sentimentalScore = sentimentalScore

    def __hash__(self): 
        hashStr = ("14" 
                    +str(self.date).replace('-',''))
        return int(hashStr)
            
    @property
    def date(self)->DateRepresentation:
        return self.__date
    
    @date.setter
    def date(self,val):
        self.__date = DateRepresentation(val)

    @property
    def correspondingGroupElement(self)->type[Element]:
        return NewsElement        
            
    @property
    def sentimentalScore(self)->float: 
        return self.__sentimentalScore
    
    @sentimentalScore.setter
    def sentimentalScore(self,val):
        try: 
            floatScore = float(val)
            self.__sentimentalScore = floatScore
        except:
            self.__sentimentalScore = None

    
    def valid(self):
        return (DateRepresentation.isValid(self.date) 
                and isinstance(self.sentimentalScore,float))
    
    @classmethod
    def getGroupElement(cls, points:list[NewsDataPoint])->NewsElement:
        return NewsElement(points)

    def getTypeGroupElement(cls)->type[Element]:
        return NewsElement
    
    

class NewsElement(Element):
    def __init__(self,points:list[NewsDataPoint]=[]):
        self.__inDict = points        
    
    @property
    def pointType(self)->type[DataPoint]: 
        return NewsDataPoint
    
    @property
    def __inDict(self)->dict[int,NewsDataPoint]:
        return self.__element
    
    @__inDict.setter
    def __inDict(self,val:list[NewsDataPoint]): 
        validPoints = dict()
        for iPoint in val: 
            if isinstance(iPoint,NewsDataPoint):
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
        
    
    def acceptVistor(self,v):
        return v.visitNewsElement(self)
    
    def acceptOutVistor(
        self,
        v,
        dest:str): 
        return v.visitOutNewsElement(self,dest)

                
    @classmethod
    def convertible(cls,targetClass:type[Element])->bool:
        return False 
    
    
    def convertTo(self,targetTemplate:Element | type[Element])->Element:
        pass     
    
    def getPointFrom(self,date:DateRepresentation)->NewsDataPoint: 
        hashStr = ("14" 
                    +str(date).replace('-',''))
        return self.__inDict.get(int(hashStr),NoneDataPoint)
    
    
    @classmethod
    def getConveribleClasses(cls)->list[type[Element]]:
        return []        

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