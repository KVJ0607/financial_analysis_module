from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping,Callable
from typing import Type

from shareEntity import ShareEntity
from point import DataPoint,GroupElement,NoneDataPoint,NoneElement,CarNDataPoint,CarNElement,NewsNewsDataPoint,NewsNewsElement,PricingDataPoint,PricingElement
from date_utils import DateRepresentation
from .utils.reorderOperand import ReorderOperand




class CollectionGroup:   

    def __init__(
        self,
        shareCode:ShareEntity|str =None,
        *args,
        ):
        
        self.initCayleyTable()
        self.updateCayleyTable(*args)
        self.updateCayleyTable()                              

        
        self.shareEntity = shareCode
            
    
    @property
    def shareEntity(self)->ShareEntity: 
        return self.__shareEntity
    
    @shareEntity.setter
    def shareEntity(self,share): 
        self.__shareEntity = ShareEntity.createShareCode(share)
    
    
    @property
    def shareCode(self)->str: 
        return self.__shareEntity.shareCode    
    
    @shareCode.setter
    def shareCode(self,share): 
        self.__shareEntity = ShareEntity.createShareCode(share)
                  
                

    @property
    def cayleyTable(self)->Mapping[type[DataPoint],'CollectionGroup']:
        return self.__cayleyTable
    
                
    def initCayleyTable(self):
        cayleyTable = {}
        for iType in DataPoint.__subclasses__(): 
            cayleyTable[iType] = NoneDataPoint.getGroupElement()
        self.__cayleyTable = cayleyTable

    def updateCayleyTable(self,*args):        
        self.__updateCayleyTable2(0,*args)
        
    def __updateCayleyTable2(self,loopNumber,*args):       
        
        ###part One: fill the element of class with actual element 
        gElements = list(args)
        if len(gElements)!= 0:
            for iEle in gElements:
                if not isinstance(iEle,GroupElement):
                    raise TypeError(f"gElement is of type{type(iEle)} but not {GroupElement}")
                
                if iEle.eleClass in self.__cayleyTable: 
                    self.__cayleyTable[iEle.eleClass] = iEle
                else: 
                    raise ValueError(f"The class {iEle} doesn't belong to the group")
                
        ##Part Two: get the dot product of all possibility                
        for iClass, iEle in self.cayleyTable.items(): 
            if type(iEle) != NoneElement:                
                for jClass,jEle in self.cayleyTable.items():                
                    iEle:GroupElement
                    jEle:GroupElement
                    if type(jEle) != NoneElement:                    
                        self.dot(iClass,jClass)
                    elif iEle.convertible(jClass):
                        self.cayleyTable[jClass] = (iEle.convertTo(jClass))    
       
       ##Part Three: The produced element from part two should be dotted one more time                      
        ### Important don't swap the order    
        loopNumber+=1
        ###
        ###
        if loopNumber <2:
            self.__updateCayleyTable2(loopNumber)
        ###            
        
    def expandCayleyTable(self,gElement:GroupElement): 
        if not isinstance(gElement,GroupElement):
            raise TypeError(f"gElement is of type{type(gElement)} but not {GroupElement}")        
        self.__cayleyTable[gElement.eleClass] = gElement
        
    def expandGroup(self,elementClass:type[DataPoint]): 
        self.__cayleyTable[elementClass] = NoneDataPoint.getGroupElement()
        self.updateCayleyTable()
      
         
                    
            
    def containElementClass(self,eleClass:Type[DataPoint])->bool:
        """
        Check if the collection group contain the element
        """
        if eleClass in self.__cayleyTable: 
            return True
        else: 
            return False        
        
        
    def getElement(self,eleClass:Type[DataPoint])->GroupElement:        
        """
        Get the element of the collection group
        """
        if eleClass in self.__cayleyTable: 
            return self.__cayleyTable[eleClass]
        else: 
            raise ValueError(f"The element Class {eleClass.__name__} doesn't belong to the group")
    
                                
    
    def dot(self,classA:type[DataPoint],classB:type[DataPoint]):
        if (classA not in DataPoint.__subclasses__()
            or classB not in DataPoint.__subclasses__()):
            raise TypeError(f"""{classA} and {classB} should be 
                            of a class whoses parent class is 
                            {DataPoint}""")
            
        for subClass in HeterogCollectionOperator.__subclasses__(): 
            if (subClass.match(classA,classB)
                and not self.containElementClass(
                    subClass.pointClassToBeReturned)
                ):
                targetEle = subClass.dot(
                    self.getElement(classA),
                    self.getElement(classB))     
                self.expandCayleyTable(targetEle)
                                                 

                 
            
    def joinGroupTable(self,groupB:CollectionGroup):    
        if not isinstance(groupB,CollectionGroup):
            raise TypeError(f"""{groupB} should be of 
                            class {CollectionGroup} but 
                            not {type(groupB)}""")
        
        elementsToBeUpdates = []
        for key,value in groupB.cayleyTable.items(): 
            if (key in self.cayleyTable 
                and (not isinstance(value,NoneElement))
                and isinstance(self.getElement(key),NoneElement)): 
                elementsToBeUpdates.append(value)                
        self.updateCayleyTable(*elementsToBeUpdates)    

    @classmethod
    def operateOfelementInClassSpace(
        self,
        groupA:CollectionGroup,
        groupB:CollectionGroup,
        spaceOfClass:type[DataPoint])->GroupElement:
        
        if not groupA.containElementClass(spaceOfClass): 
            groupA.expandCayleyTable(
                
            )
        
        
        spaceElementA = groupA.getElement(spaceOfClass)
        spaceElementB = groupB.getElement(spaceOfClass)
        if isinstance(spaceElementA,NoneElement): 
            raise ValueError(f"""{groupA} don't have point class 
                             {spaceOfClass} data""")
        elif isinstance(spaceElementB,NoneElement): 
            raise ValueError(f"""{groupA} don't have point class {
                spaceOfClass} data""")
            
        

            

class CollectionsNotHomogeneousError(Exception):
    def __init__(self,message,code=None):
        self.message = message
        self.code = code
    
    def __str__(self):  
        if self.code:
            return f"CollectionsNotHomogeneousError: {self.message} (Error code: {self.code})"
        else:
            return f"CollectionsNotHomogeneousError: {self.message}"    
                        

class PointTypeInconsistentError(Exception):
    def __init__(self, 
                 message='Not all the data points in the collection are the same class', 
                 code=None):
        self.message = message
        self.code = code

    def __str__(self):        
        if self.code:
            return f"PointTypeInconsistentError: {self.message} (Error code: {self.code})"
        else:
            return f"PointTypeInconsistentError: {self.message}"       
        



class HeterogCollectionOperator(ABC) :     
    """ 
    Handle binary opertaion between object of DataCollection with the 
    different pointType attribute.The actual logic depends on the pointType attribute 
    from both operand.
        
    A class that provide classmethods that acts as operators between dataCollections 
    having different pointType attribute.
    """
    
    @property
    @abstractmethod
    def pointClassToBeReturned(self):
        pass 
        
        
    @classmethod
    @abstractmethod
    def match(
        cls,
        classA:type[DataPoint],
        classB:type[DataPoint])->bool: 
        """
        Check if the two DataCollection are compatible 
        for the operator. 
        """
        pass


    @classmethod
    @abstractmethod
    def dot(
        cls,
        leftOperand:GroupElement,
        rightOperand:GroupElement)->GroupElement:
        """
        The dot method is a classmethod that acts as a operator 
        ofdataCollections  group. It will return a new
        DataCollection with the result of the operation.
        """
        pass
    
    
class CarNewsOperators(HeterogCollectionOperator): 
    """
    A class that provide a classmethod that acts as a operator between dataCollections 
    with cars and news data points.    
    """

    @property
    def pointClassToBeReturned(self):
        return self.CarsNewsDataPoint         

    @classmethod
    def match(
        cls,
        classA:type[DataPoint],
        classB:type[DataPoint])->bool:
        eSignature = set([classA,classB])
        for iSignature in cls.signature(): 
            if iSignature == eSignature: 
                return True
        return False
        
    
    @classmethod
    def dot(
        cls,
        gEleA:GroupElement,
        gEleB:GroupElement,
        )->GroupElement: 
        eSignature = set([gEleA.eleClass,gEleB.eleClass])    
        for iSignature in cls.signature():
            if iSignature == eSignature: 
                if eSignature == set([CarNDataPoint,NewsNewsDataPoint]):
                    return cls.__defaultOperator(gEleA,gEleB)  
                elif eSignature == set([PricingDataPoint,NewsNewsDataPoint]):
                    return cls.__pricingOperator(gEleA,gEleB)
                
            
        
    
    @classmethod
    def signature(cls)->list[set]: 
        signatures = []
        signatures.append(set([CarNDataPoint,NewsNewsDataPoint]))
        signatures.append(set([PricingDataPoint,NewsNewsDataPoint]))
        return signatures
    
    
    @classmethod
    def __defaultOperator(
        cls,
        gEleA:GroupElement,
        gEleB:GroupElement) -> GroupElement:                        
        carEle:CarNElement = None 
        newsEle:NewsNewsElement = None
                
        if (gEleA.eleClass == CarNDataPoint
            and gEleB.eleClass == NewsNewsDataPoint): 
            carEle = gEleA 
            newsEle = gEleB
        elif (gEleB.eleClass == CarNDataPoint
            and gEleA.eleClass == NewsNewsDataPoint): 
            carEle = gEleB
            newsEle = gEleA
        else: 
            raise TypeError(f"""{gEleA} and {gEleB}
                            are of type {type[gEleA]}
                            and {type[gEleB]}, but not 
                            {CarNElement} and {NewsNewsElement}""")
        
        
        carNewsDataPoints = []
        try:
            for carHash,carPoint in carEle.element.items():                 
                previousDate = carPoint.previousDate
                followingDate = carPoint.followingDate                 
                accumlatedSentimentalScore = 0                    
                for iTime in DateRepresentation.getDateRange(previousDate,followingDate): 
                    iDataPoint = newsEle.getPointFrom(iTime)
                    accumlatedSentimentalScore += iDataPoint.sentimentalScore
                carNewsDataPoints.append(
                    CarNewsOperators.CarsNewsDataPoint(
                        carPoint,
                        accumlatedSentimentalScore)
                )                        
        except Exception as e: 
            print(F"Error: {gEleA.eleClass} and {gEleB.eleClass}")
            raise e
                
        return CarNewsOperators.CarsNewsDataPoint.getGroupElement(carNewsDataPoints)
        
    
    @classmethod
    def __pricingOperator(
        cls,
        gEleA:GroupElement,
        gEleB:GroupElement) -> GroupElement:         
        if gEleA.eleClass == PricingDataPoint: 
            return cls.__defaultOperator(
                gEleA.convertTo(CarNDataPoint),
                gEleB)
        else: 
            return cls.__defaultOperator(
                gEleB.convertTo(CarNDataPoint),
                gEleA)            
            

    
    class CarsNewsDataPoint(DataPoint):
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
            return CarNDataPoint.__hash__()*1000+NewsNewsDataPoint.__hash__()
        
        @property
        def date(self)->DateRepresentation:
            return self.carN.date
        
        def valid(self)->bool:  
            return (self.date.isValid() 
                    and isinstance(self.accumlatedSentimentalScore,float))
            
        @classmethod            
        def equivalent(cls,*arg)->bool: 
            coordinates = set()
            for iPoint in arg:
                if not isinstance(iPoint,'CarNewsOperators.CarsNewsDataPoint'): 
                    return False
                coordinates.add(iPoint.carN.coordinate)
            return len(coordinates) == 1
        
        @classmethod
        def getGroupElement(cls,points:list['DataPoint'])->'CarNewsOperators.CarsNewsElement': 
            return  CarNewsOperators.CarsNewsElement(points)
        
    class CarsNewsElement(GroupElement):
        
        def __init__(self,points:list[CarNewsOperators.CarsNewsDataPoint]):
            self.element = points 
            
        @property
        def eleClass(self)->type[DataPoint]: 
            return CarNewsOperators.CarsNewsDataPoint
        
        @property
        def element(self)->dict[str,CarNewsOperators.CarsNewsDataPoint]:
            return self.__element
        
        @element.setter
        def element(self,val:list[CarNewsOperators.CarsNewsDataPoint]): 
            validPoints = dict()
            for iPoint in val: 
                if iPoint.valid() and isinstance(iPoint,CarNewsOperators.CarsNewsDataPoint):
                    validPoints[iPoint.carN.coordinate] = iPoint
            self.__element = validPoints            
            
        
        def convertible(self,targetClass:type[DataPoint])->bool:
            return False 
        
        def convertTo(self,targetClass:type[DataPoint])->'GroupElement':
            pass          
            

        
        
                 