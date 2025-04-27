from __future__ import annotations

from abc import ABC,abstractmethod
from collections.abc import Mapping
from typing import Tuple, Type

from shareEntity import ShareEntity
from point import DataPoint,NoneDataPoint,CarNDataPoint,NoneDataPoint,NewsNewsDataPoint,HistoricalDataPoint
from date_utils.dateRepresentation import DateRepresentation




class DataCollection:  
    """Collection of DataPoint of the same implementation type"""       
    def __init__(
        self,dataPoints:list[DataPoint],
        shareCode:ShareEntity|str =None):
        
        self.__notSamePointType_RaiseError(dataPoints)                                
        
        self.dataPoints = dataPoints
        self.shareEntity = shareCode
        
        self.__interacted = False
        self.__containNewWindow =False

    
    @property
    def pointType(self)->Type[DataPoint]:     
        firstDataPoint = next(iter(self.__dataPoints.values()))
        return type(firstDataPoint)    
    
    
    @property 
    def coordinates(self)->set:
        if self.__interacted: 
            return self.__interactedCoordinates
        else:
            return set(self.__dataPoints.keys())


    @property
    def dataPoints(self)->Mapping[str,DataPoint] | DataCollection: 
        if self.__interacted and self.__containNewWindow:
            return self.newWindow 
        elif self.__interacted and not self.__containNewWindow:
            return {key:value for key,value in self.__dataPoints 
                if key in self.interactedCoordinates}            
        else:
            return self.__dataPoints        
    
    @dataPoints.setter
    def dataPoints(self,rawDataPointList:list[DataPoint]):
        self.__dataPoints = self._getValidCollectionMap(rawDataPointList)
                    

    @property
    def uninteractedDataPoint(self)->Mapping[str,DataPoint]:
        return self.__dataPoints
    
    def __setValidDataPoint(self,DataPointList:list[DataPoint]):
        self.__dataPoints = DataPointList
    
    
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
    def newWindow(self)->'DataCollection':
        if self.__containNewWindow:
            return self.__newWindow
        else: 
            return self
    
    @newWindow.setter
    def newWindow(self,val:'DataCollection'): 
        self.__interacted = True
        self.__containNewWindow = True
        self.__newWindow = val
    
    @property
    def interactedCoordinates(self)->set[str]:         
        if self.__interacted: 
            return self.__interactedCoordinates
        else: 
            return set(self.__dataPoints.keys())
    
    @interactedCoordinates.setter
    def interactedCoordinates(self,coor:list[str]): 
        #Added an extra step ensure the coordinates intersection 
        #is a subset of the instance's coordinates
        oldFlag = self.__interacted
        try:
            self.__interactedCoordinates = set.intersection(
                set(coor),set(self.dataPoints.keys()))
            self.__interacted = True
        except Exception as e: 
            self.__interacted = oldFlag
            raise e 
    
        
    
    def getDataPointFromCoordinate(self, coordinate:str)->DataPoint:
        return self.dataPoints[coordinate]    
    

    def joinWithoutOverWrite(self,*args):
        """
        args: collections of the same point type and the same share 
        It update the collection with collections in the args, 
        while keep the arg collections unchanged        
        """
        try:
            self.__samePointType(args)
            self.__sameShareEntity(args)
        except(CollectionsNotHomogeneousError): 
            raise ValueError("""The arguments have to be a list of 
                DataCollection of the same pointType attribute""")        
        
        newData = map()
        foundKeys = set()
        for iColl in args: 
            iColl:DataCollection
            if len(foundKeys) == 0: 
                foundKeys = iColl.coordinates
                newData = iColl.dataPoints
            else: 
                for jCoor in iColl.coordinates.difference(foundKeys): 
                    newData[jCoor] = iColl.getDataPointFromCoordinate(jCoor)
                    foundKeys.add(jCoor)
        self.__setValidDataPoint(newData)
    
    def joinWithOverWrite(self,*args):
        """
        args: collections of the same point type and the same share 
        It update the collection with collections in the args, 
        while keep the arg collections unchanged        
        """        
        self.__samePointType(args)
        self.__sameShareEntity(args)
        
        newData = map()
        foundKeys = set()
        for iColl in args: 
            iColl:DataCollection
            if len(foundKeys) == 0: 
                foundKeys = iColl.coordinates
                newData = iColl.dataPoints
            else: 
                for jCoor in iColl.coordinates: 
                    newData[jCoor] = iColl.getDataPointFromCoordinate(jCoor)
                    foundKeys.add(jCoor)
        self.__setValidDataPoint(newData)                    

                    
    
    def interact(
                self,*args,
                clearPreviousInersection = False):
        
        homoSet = self.getHomoColls(*args)
        hetroSet = set(args).difference(homoSet)    
        self.interactHomo(homoSet,clearPreviousInersection=clearPreviousInersection)
        for iColl in hetroSet:
            iColl:DataCollection
            self.interactHetro(iColl)
            
            
    def interactHomo(self,homoSet:list[DataCollection],
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
        
    
    def interactHetro(
            self,operant:'DataCollection'):                
        signature = self.getSignatureFromDuoCollection(operant,self)  
        found = False 
        for subcls in HeterogCollectionOperator.__subclasses__(): 
            if signature == subcls.signature():       
                found = True
                print(f"Found {signature} and {subcls.signature}")
                if subcls.needNewWindow():                                                 
                    self.newWindow = subcls.createNewWindow(operant,self)
                else: 
                    subcls.interact(operant,self)  
            if not found:      
                print(f"Warning: No operator is defined for {signature} and {subcls.signature}")   
    
    def getHomoColls(self,*args)->list[DataCollection]:                
        homoSet = list()
        for iColl in args:
            iColl:DataCollection
            if iColl.pointType == self.pointType:
                homoSet.append(iColl)
        return homoSet
    
    
    @staticmethod
    def cloneNewWindow(collections:list['DataCollection']):
        targetWindow = collections[0].newWindow
        for iColl in collections[1:]: 
            iColl:DataCollection            
            iColl.newWindow = targetWindow
    
    
    @staticmethod 
    def getSignatureFromDuoCollection(
            collectionA:'DataCollection',collectionB:'DataCollection'): 
        """Provide a signature used to get the corresponding 
        class for the binary operation. 
        collectionA, collectionB are two data collection 
        and the order is irrelevant. 
        """                             
        return set([collectionA.pointType.__name__,collectionB.pointType.__name__])
    
    
    @staticmethod 
    def clearPreviousInersection(collections:list[DataCollection]): 
        for iColl in collections: 
            iColl.__interacted = False
            

    @staticmethod
    def __samePointType(collections:list[DataCollection])->bool:
        pointType = collections[0].pointType
        for iColl in collections: 
            if iColl.pointType != pointType: 
                return False
        return True
    
    @staticmethod
    def __sameShareEntity(*args)->bool: 
        inputColls: list[DataCollection]
        inputColls = list(args)
        shareEntity = inputColls[0].shareEntity
        for iColls in inputColls: 
            if iColls.shareEntity != shareEntity:
                return False
        return True 
    
    @staticmethod
    def __notSamePointType_RaiseError(datapoints:list[DataPoint])->bool: 
        if len(datapoints) == 0: 
            raise PointTypeInconsistentError()
        pointType = type(datapoints[0])
        for currPoiunt in datapoints: 
            if type(currPoiunt) != pointType: 
                return False
        return True


    

    @classmethod
    def _getValidCollectionMap(cls,dataPoints:list[DataPoint])->Mapping[str,DataPoint]:        
        completeMap = {}
        if len(dataPoints) == 0:             
            return {}
        pointType = type(dataPoints[0])
        for currentDataPoint in dataPoints: 
            if pointType != type(currentDataPoint): 
                raise PointTypeInconsistentError()
            if currentDataPoint.valid():
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
    
    __leftOperand = NoneDataPoint
    __rightOperand = NoneDataPoint
    
    @classmethod
    @abstractmethod
    def needNewWindow(cls)->bool: 
        pass
    
    @classmethod
    @abstractmethod        
    def signature(cls)->set: 
        pass
    
    @classmethod        
    @abstractmethod
    def interact(
        cls,operandA:DataCollection,
        operandB:DataCollection)->DataCollection: 
        """
        Interact the two DataCollection according 
        to the logic for their point type.
        
        """        
        pass 
    
    @classmethod    
    @abstractmethod
    def createNewWindow(
            cls,operandA:DataCollection,
            operandB:DataCollection)->DataCollection: 
        """
        output a new DataCollection using a function 
        according to their point type.
        
        """
        pass 
    
    

    
    @classmethod
    def __getLeftOperandPointType(cls)->Type[DataPoint]: 
        '''
        Built to meet the non-communcative property.
        Raise error if not implemented
        '''        
        raise NotImplementedError ("left operand is not implemented")
        
    
    @classmethod
    def __getRightOperandPointType(cls)->Type[DataPoint]:  
        '''
        Built to meet the non-communcative property.
        Raise error if not implemented
        '''        
        raise NotImplementedError ("right operand is not implemented")
        
    
    @classmethod
    def __matchingOperand(cls,
                        leftInputCollection:DataCollection,
                        rightInputCollection:DataCollection)->tuple[DataCollection]: 
        """
        All opertors are implictly non-communicative and are only defined for 
        a specified ordered. This method take two operands and return 
        them in a required oreder in a tuple.      
        """
        leftOperandType = cls.__getLeftOperandPointType()
        rightOperandType = cls.__getRightOperandPointType()
        leftInputType = leftInputCollection.pointType
        rightInputType = leftInputCollection.pointType
        
        if leftInputType == leftOperandType and rightInputType == rightOperandType: 
            return leftInputCollection,rightInputCollection
        elif rightInputType == leftOperandType and leftInputType == rightOperandType: 
            return rightInputCollection,leftInputCollection
        else: 
            raise TypeError(f'''The two input should be of types {leftOperandType} and {rightOperandType}.
                            However, the arugments are of types {leftInputType} and {rightInputType}''')
    
class CarNewsOperators(HeterogCollectionOperator): 
    """
    A class that provide a classmethod that acts as a operator between dataCollections 
    with cars and news data points.

    
    """
    __leftOperand = CarNDataPoint 
    __rightOperand = NewsNewsDataPoint
    
    @classmethod
    def needNewWindow(cls)->bool: 
        return True
    
    @classmethod
    def signature(cls)->set: 
        return set([CarNDataPoint.__name__,NewsNewsDataPoint.__name__])          
    
    @classmethod
    def interact(cls): 
        pass 
    
    @classmethod
    def createNewWindow(cls, leftOperand:DataCollection,
             rightOperand:DataCollection) -> DataCollection:
        carCollection: DataCollection
        newsCollection: DataCollection
        
        carCollection,newsCollection = cls.__matchingOperand(leftOperand,rightOperand)        
        
        carNewsDataPoints = []
        
        for carCoordinate,carPoint in carCollection.dataPoints: 
            carCoordinate:str
            carPoint:CarNDataPoint
            
            previousDate = carPoint.previousDate
            followingDate = carPoint.followingDate
            carDate = carPoint.date
                 
            accumlatedSentimentalScore = 0                    
            for iTime in DateRepresentation.getListOfDateStrWithinTwoDates(previousDate,followingDate): 
                iDataPoint = newsCollection.getDataPointFromCoordinate(NewsNewsDataPoint.getCoordinateFrom(iTime))
                accumlatedSentimentalScore += iDataPoint.getDataValueWithAttribute(NewsNewsDataPoint.enum()[1])
                
            attriList = ['sentimentalScore']                
            carNewsDataPoints.append(HistoricalDataPoint(carDate,attriList,[accumlatedSentimentalScore],attriList))
        
        return DataCollection(carNewsDataPoints,carCollection.shareEntity)     
            
        
                 