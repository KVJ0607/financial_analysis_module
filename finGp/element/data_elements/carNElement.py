from __future__ import annotations

from ...date_utils import DateRepresentation
from ...element.element import DataPoint,Element

class CarNDataPoint(DataPoint):     
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
    def correspondingGroupElement(self)->type[Element]:
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
    def getTypeGroupElement(cls)->type[Element]:
        return CarNElement 


            
class CarNElement(Element):
    def __init__(self,points:list[CarNDataPoint]=[],interval=3):
        self.__inDict = points        
        self.interval = interval

    @property
    def pointType(self)->type[DataPoint]: 
        return CarNDataPoint
    
    @property
    def __inDict(self)->dict[int,CarNDataPoint]:
        return self.__inDict
    
    @__inDict.setter
    def __inDict(self,val:list[CarNDataPoint]): 
        validPoints = dict()
        count = 0
        for iPoint in val: 
            
            if isinstance(iPoint,CarNDataPoint):
                count +=1                  
                if iPoint.valid():              
                    validPoints[iPoint.__hash__()] = iPoint
        self.__inDict = validPoints

    @property
    def items(self):
        """
        Returns an iterable view of (key, DataPoint) pairs contained in this Element,
        allowing iteration over all DataPoints.
        """
        return self.__inDict.items()

    
    @property
    def interval(self)->int: 
        return self.__interval    
    
    @interval.setter
    def interval(self,nDay:int): 
        if nDay//2 == 0: 
            raise ValueError("nDay should be an odd number")
        if nDay < 1: 
            raise ValueError("nDay should be a positive number")
        self.__interval = nDay 

    
    def acceptVistor(self,v):
        return v.visitCarNElement(self)            

    def acceptOutVistor(
        self,
        v,
        dest:str): 
        return v.visitOutCarNElement(self,dest)
            
    @classmethod
    def convertible(cls,targetClass:type[Element])->bool:
        return False 
    
    
    def convertTo(self,targetTemplate:Element | type[Element])->Element:
        pass     
    
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
    
    