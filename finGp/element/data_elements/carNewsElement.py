from __future__ import annotations

from ...date_utils import DateRepresentation
from .. import DataPoint,Element,CarNDataPoint,CarNElement,NoneDataPoint

    
class CarNewsDataPoint(DataPoint):
    def __init__(self,carN,accumlatedSentimentalScore:float):
        if isinstance(carN,CarNDataPoint):
            self.carN = carN
        else:
            self.carN = NoneDataPoint
        try:                
            self.accumlatedSentimentalScore = float(accumlatedSentimentalScore)
        except: 
            self.accumlatedSentimentalScore = None
        
    def __hash__(self): 
        return self.carN.__hash__()
    
    @property
    def date(self)->DateRepresentation:
        return self.carN.date
    
    def valid(self)->bool:  
        return (self.date.isValid() 
                and isinstance(self.accumlatedSentimentalScore,float))        
    
    @classmethod
    def getGroupElement(
        cls,
        points:list[CarNewsDataPoint])->CarNewsElement: 
        return  CarNewsElement(points)


    
class CarNewsElement(Element):
    
    def __init__(self,points:list[CarNewsDataPoint]=[]):
        self._i_nDict = points 
        
    @property
    def pointType(self)->type[DataPoint]: 
        return CarNewsDataPoint
    
    @property
    def __inDict(self)->dict[str,CarNewsDataPoint]:
        return self.__element
    
    @__inDict.setter
    def __inDict(self,val:list[CarNewsDataPoint]): 
        validPoints = dict()
        for iPoint in val: 
            if iPoint.valid() and isinstance(iPoint,CarNewsDataPoint):
                validPoints[iPoint.__hash__()] = iPoint
        self.__element = validPoints            


    @property
    def items(self):
        """
        Returns an iterable view of (key, DataPoint) pairs contained in this Element,
        allowing iteration over all DataPoints.
        """
        return self.__inDict.items()
    



        
    def acceptVistor(self,v):
        return v.visitCarsNewsElement(self)  

   
    def acceptOutVistor(
        self,
        v,
        dest:str): 
        return v.visitOutCarsNewsElement(self,dest)        
        

    @classmethod
    def convertible(cls,targetClass:type[Element])->bool:
        return False 
    
    def convertTo(self,targetTemplate:Element | type[Element])->'Element':
        pass     
         
    @classmethod
    def getConveribleClasses(cls)->list[type[DataPoint]]:
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
        
        
                 