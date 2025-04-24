from collections.abc import Mapping
from typing import Tuple, Type

from shareEntity import ShareEntity
from point import DataPoint,NoneDataPoint
from .collection_manipulation.heteroOperator import HeterogCollectionOperator



class DataCollection:  
    """Collection of DataPoint of the same implementation type"""       
    def __init__(
        self,dataPoints:list[DataPoint],
        shareCode:ShareEntity|str =None):
        
        self.__notSamePointType_RaiseError(dataPoints)                                
        
        self.dataPoints = dataPoints
        self.shareEntity = shareCode
        
        self.interacted = False
        self.needNewWindow =False

    
    @property
    def pointType(self)->Type[DataPoint]: 
        return type(self.__dataPoints.values()[0])    
    
    
    @property 
    def coordinates(self)->set:
        if self.interacted: 
            return self.__coordinatesIntersection
        else:
            return set(self.__dataPoints.keys())


    @property
    def dataPoints(self)->Mapping[str,DataPoint] | 'DataCollection': 
        if self.interacted and self.needNewWindow:
            return self.newWindow 
        elif self.interacted and not self.needNewWindow:
            return {key:value for key,value in self.__dataPoints 
                if key in self.coordinatesIntersection}            
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
    def interacted(self)-> bool: 
        return self.__interacted    
    
    @interacted.setter
    def interacted(self,boolVal):
        self.__interacted = boolVal
     
    @property
    def needNewWindow(self)->bool: 
        return self.__needNewWindow
    
    @needNewWindow.setter
    def needNewWindow(self,val:bool): 
        self.__needNewWindow = val

    @property
    def newWindow(self)->'DataCollection':
        if self.needNewWindow:
            return self.__newWindow
        else: 
            return self
    
    @newWindow.setter
    def newWindow(self,val:'DataCollection'): 
        self.__newWindow = val
    
    @property
    def coordinatesIntersection(self)->set[str]:         
        if self.interacted: 
            return self.__coordinatesIntersection
        else: 
            return set(self.__dataPoints.keys())
    
    @coordinatesIntersection.setter
    def coordinatesIntersection(self,coor:list[str]): 
        #Added an extra step ensure the coordinates intersection 
        #is a subset of the instance's coordinates
        oldFlag = self.interacted
        try:
            self.__coordinatesIntersection = set.intersection(
                set(coor),set(self.dataPoints.keys()))
            self.interacted = True
        except Exception as e: 
            self.interacted = oldFlag
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

                    
     
      
      
    @classmethod
    def compare(cls,*args,
            clearPreviousInersection = False):
        
        try:
            cls.__samePointType(args)
        except(CollectionsNotHomogeneousError): 
            raise ValueError("""The arguments have to be a list of 
                DataCollection of the same pointType attribute""")
        
        if clearPreviousInersection:
            cls.clearPreviousInersection(args)
            
        coordinateIntersection = cls.__getCoordinateIntersection(*args)        
        inputColls:list[DataCollection]
        inputColls = list(args)
        for iColl in inputColls: 
            iColl.coordinatesIntersection = coordinateIntersection
            
    
            
    @classmethod
    def interact(
            cls,operantA:'DataCollection',operantB:'DataCollection'):                
        signature = cls.getSignatureFromDuoCollection(operantA,operantB)        
        for subcls in HeterogCollectionOperator.__subclasses__(): 
            if signature == subcls.signature:         
                if subcls.needNewWindow:                                                 
                    newWindow = subcls.createNewWindow(operantA,operantB)
                    operantA.newWindow = newWindow
                    operantB.newWindow = newWindow 
                else: 
                    subcls.interact(operantA,operantB)    
                        

                
            
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
    def clearPreviousInersection(*args): 
        inputColls:list[DataCollection]
        inputColls = list(args)
        for iColl in inputColls: 
            iColl.interacted = False
            

    @staticmethod
    def __samePointType(*args)->bool:
        inputColls: list[DataCollection]         
        inputColls = list(args)
        pointType = inputColls[0].pointType
        for iColl in inputColls: 
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


    @staticmethod 
    def __getCoordinateIntersection(cls,*args):
        dataColls:list[DataCollection]
        dataColls = list(args)
        return set.intersection([x.coordinatesIntersection for x in dataColls]) 
    

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