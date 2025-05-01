from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping,Callable
from typing import Type

from shareEntity import ShareEntity
from point import DataPoint,NoneDataPoint,CarNDataPoint,NoneDataPoint,NewsNewsDataPoint,HistoricalDataPoint,PricingDataPoint
import date_utils
from .utils.reorderOperand import ReorderOperand




class CollectionGroup:  
    """Collection of DataPoint of the same implementation type"""       


    def __init__(
        self,
        dataPoints:list[DataPoint],
        shareCode:ShareEntity|str =None):
        
        self.initCayleyTable()
        self.updateCayleyTable(dataPoints)                              
    
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
    def cayleyTable(self)->Mapping[str,'CollectionGroup']:
        return self.__cayleyTable
    
                
    def initCayleyTable(self):
        cayleyTable = {}
        for iType in DataPoint.__subclasses__(): 
            cayleyTable[iType.__name__] = None
        self.__cayleyTable = cayleyTable

    def updateCayleyTable(self,element:list[DataPoint]):
        """
        Update the look up table with the data collection
        """
        
        thisElementClass = self.__returnElementClass_OrRaiseError(element).__name__
        
        if thisElementClass in self.__cayleyTable: 
            self.__cayleyTable[thisElementClass] = element
        else: 
            raise ValueError(f"The class {thisElementClass} doesn't belong to the group")
            
    def containElement(self,eleClass:Type[DataPoint])->bool:
        """
        Check if the collection group contain the element
        """
        if eleClass.__name__ in self.__cayleyTable: 
            return True
        else: 
            return False        
        
    def getElement(self,eleClass:Type[DataPoint])->list[DataPoint]:        
        """
        Get the element of the collection group
        """
        if eleClass.__name__ in self.__cayleyTable: 
            return self.__cayleyTable[eleClass.__name__]
        else: 
            raise ValueError(f"The point type {eleClass.__name__} is not in the look up table")
    
    
                     

    def convertToCarNColl(self,nDay:int=3): 
        if self.pointType != PricingDataPoint:
            raise TypeError(f"Only DataCollection of type{PricingDataPoint.__name__} but not {self.pointType.__name__}")
        if nDay//2 == 0: 
            raise ValueError("nDay should be an odd number")
        if nDay < 1: 
            raise ValueError("nDay should be a positive number")
        nDay = (nDay-1)/2 
            
        
        dateList = self.dates
        dateList = sorted(dateList)
        
        carNPoints:list[CarNDataPoint] = [] 
        for iDay in date_utils.DateRepresentation.getDateRange(dateList[1],dateList[-1]):
            if iDay+nDay in dateList and iDay-nDay in dateList:
                lastPoint:PricingDataPoint = self.getPointFromElement(PricingDataPoint.getCoordinateFrom(iDay-nDay))
                nextPoint:PricingDataPoint = self.getPointFromElement(PricingDataPoint.getCoordinateFrom(iDay+nDay))
                carNPoints.append(CarNDataPoint(
                    iDay,
                    iDay-nDay,
                    iDay+nDay,
                    (nextPoint.adjClose-lastPoint.adjClose)/lastPoint.adjClose,
                    nDay)
                )
        self.updateCayleyTable(CollectionGroup(carNPoints,self.shareEntity))
        
    
    def interact(
                self,*args,
                clearPreviousInersection = False):
        
        homoSet = self.__getHomoColls(*args)
        hetroSet = set(args).difference(homoSet)    
        self.__interactHomo(homoSet,clearPreviousInersection=clearPreviousInersection)
        for iColl in hetroSet:
            iColl:CollectionGroup
            self.__interactHetro(iColl)
            
            
    def __interactHomo(self,homoSet:list[CollectionGroup],
            clearPreviousInersection = False):        
        try:
            self.__samePointType(homoSet)
        except(CollectionsNotHomogeneousError): 
            raise ValueError("""The arguments have to be a list of 
                DataCollection of the same pointType attribute""")
        
        if clearPreviousInersection:
            self.clearPreviousInersection(homoSet)        

        
        interactedCoordinates = self.coordinates
        for iColl in homoSet: 
            interactedCoordinates.intersection_update(iColl.coordinates)
        
        self.interactedCoordinates = interactedCoordinates
        
    
    def __interactHetroOld(
            self,operant:'CollectionGroup'):                
        signature = self.__getSignatureFromDuoCollection(operant,self)  
        found = False 
        for subcls in HeterogCollectionOperator.__subclasses__(): 
            if subcls.match(signature):       
                found = True                
                matchedOperator = subcls.getMatchingOperator(operant,self,signature) ## abstract away
                self.updateCayleyTable(matchedOperator(operant,self))
            if not found:      
                print(f"Warning: No operator is defined for {signature}")   

    def __interactHetro(
            self,operant:'CollectionGroup'):                
        found = False 
        for subcls in HeterogCollectionOperator.__subclasses__(): 
            if subcls.match(self,operant):       
                found = True                                                
                self.updateCayleyTable(
                    subcls.dot(operant,self)
                )
            if not found:      
                print(f"Warning: No operator is defined for {self.pointType.__name__} and {operant.pointType.__name__}")                   
    
    def __getHomoColls(self,*args)->list[CollectionGroup]:                
        homoSet = list()
        for iColl in args:
            iColl:CollectionGroup
            if iColl.pointType == self.pointType:
                homoSet.append(iColl)
        return homoSet
    

    
    
    @staticmethod 
    def __getSignatureFromDuoCollection(
            collectionA:'CollectionGroup',collectionB:'CollectionGroup'): 
        """Provide a signature used to get the corresponding 
        class for the binary operation. 
        collectionA, collectionB are two data collection 
        and the order is irrelevant. 
        """                             
        return set([collectionA.pointType.__name__,collectionB.pointType.__name__])
    
    
    @staticmethod 
    def clearPreviousInersection(collections:list[CollectionGroup]): 
        for iColl in collections: 
            iColl.__interacted = False
            

    @staticmethod
    def __samePointType(collections:list[CollectionGroup])->bool:
        pointType = collections[0].pointType
        for iColl in collections: 
            if iColl.pointType != pointType: 
                return False
        return True
    
    @staticmethod
    def __sameShareEntity(*args)->bool: 
        inputColls: list[CollectionGroup]
        inputColls = list(args)
        shareEntity = inputColls[0].shareEntity
        for iColls in inputColls: 
            if iColls.shareEntity != shareEntity:
                return False
        return True 
    
    @staticmethod
    def __returnElementClass_OrRaiseError(datapoints:list[DataPoint])->bool: 
        if len(datapoints) == 0: 
            raise PointTypeInconsistentError()
        
        correctType = type(datapoints[0])
        for currPoiunt in datapoints: 
            if type(currPoiunt) != correctType: 
                raise PointTypeInconsistentError()



    

    @classmethod
    def _getValidCollectionMap(cls,dataPoints:list[DataPoint])->Mapping[str,DataPoint]:        
        completeMap = {}
        if len(dataPoints) == 0:     
            print("Warning: The collection is empty")        
            return {}
        pointType = NoneDataPoint
        for currentDataPoint in dataPoints: 
            if pointType == NoneDataPoint: 
                pointType = type(currentDataPoint)
            elif pointType != type(currentDataPoint): 
                raise PointTypeInconsistentError()            
            elif currentDataPoint.valid():
                #If there is two dataPoint with the same coordinate,
                #the latter one with overwrite the former one
                completeMap[currentDataPoint.coordinate] = currentDataPoint  
        return completeMap                
            

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
    
    
    @classmethod
    @abstractmethod
    def match(
        cls,
        operandA:CollectionGroup,
        operandB:CollectionGroup)->bool: 
        """
        Check if the two DataCollection are compatible 
        for the operator. 
        """
        pass
    
    
    @classmethod
    @abstractmethod
    def dot(
        cls,
        leftOperand:CollectionGroup,
        rightOperand:CollectionGroup)->CollectionGroup:
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
    
    
    
    
    def __init__(self,gEleA:CollectionGroup,
                 gEleB:CollectionGroup):
        
        if self.match(gEleA,gEleB):
            if gEleA.pointType == CarNDataPoint:
                self.carNEle = gEleA
            elif gEleA.pointType == NewsNewsDataPoint:
                self.newsEle = gEleA
            else: 
                self.pricingEle = gEleA
            if gEleB.pointType == CarNDataPoint:
                self.carNEle = gEleB
            elif gEleB.pointType == NewsNewsDataPoint:
                self.newsEle = gEleB
            else:
                self.pricingEle = gEleB
        
        

    @classmethod
    def match(
        cls,
        gEleA:CollectionGroup,
        gEleB:CollectionGroup)->bool:
        eSignature = set(gEleA.pointType.__name__,gEleB.pointType.__name__)
        for iSignature in cls.signature(): 
            if iSignature == eSignature: 
                return True
        return False
    
    
    @classmethod
    def dot(
        cls,
        gEleA:CollectionGroup,
        gEleB:CollectionGroup,
        )->Callable[[CollectionGroup,CollectionGroup],CollectionGroup]: 
        thisOperator = CarNewsOperators(gEleA,gEleB)
        eSignature = set(gEleA.pointType.__name__,gEleB.pointType.__name__)    
        for iSignature in cls.signature():
            if iSignature == eSignature: 
                if eSignature == set(set([CarNDataPoint.__name__,NewsNewsDataPoint.__name__])):
                    return thisOperator.__defaultOperator()    
                elif eSignature == set([PricingDataPoint.__name__,NewsNewsDataPoint.__name__]):
                    return thisOperator.__pricingOperator()
                
            
        
    
    @classmethod
    def signature(cls)->list[set]: 
        signatures = []
        signatures.append(set([CarNDataPoint.__name__,NewsNewsDataPoint.__name__]))
        signatures.append(set([PricingDataPoint.__name__,NewsNewsDataPoint.__name__]))
        return signatures
    
    
    
    def __defaultOperator(self) -> CollectionGroup:        
        
        carEle:CollectionGroup = self.carNEle
        newsEle:CollectionGroup = self.newsEle
                
        
        carNewsDataPoints = []
        
        for carCoordinate,carPoint in carEle.dataPoints: 
            carCoordinate:str
            carPoint:CarNDataPoint
            
            previousDate = carPoint.previousDate
            followingDate = carPoint.followingDate
            carDate = carPoint.date
                 
            accumlatedSentimentalScore = 0                    
            for iTime in date_utils.DateRepresentation.getDateRange(previousDate,followingDate): 
                iDataPoint = newsEle.getPointFromElement(NewsNewsDataPoint.getCoordinateFrom(iTime))
                accumlatedSentimentalScore += iDataPoint.getValueWithAttribute(NewsNewsDataPoint.enum()[1])
                
            attriList = ['sentimentalScore']                
            carNewsDataPoints.append(HistoricalDataPoint(carDate,attriList,[accumlatedSentimentalScore],attriList))
        
        return CollectionGroup(carNewsDataPoints,carEle.shareEntity)     
    
    
    def __pricingOperator(self)->CollectionGroup: 
        self.carNEle:CollectionGroup = self.pricingEle.convertToCarNColl()
            

        
        
                 