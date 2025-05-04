   
from __future__ import annotations



from ..collectionOperator import CollectionOperator
from point import DataPoint,GroupElement,NoneDataPoint,CarNDataPoint,CarNElement,NewsNewsDataPoint,NewsNewsElement,PricingDataPoint
from date_utils import DateRepresentation


class CarNewsOperator(CollectionOperator): 
    """
    A class that provide a classmethod that acts as a operator between dataCollections 
    with cars and news data points.    
    """

    @property
    def pointClassToBeReturned(self):
        return CarsNewsDataPoint         

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
                for iTime in DateRepresentation.getDateRange(
                    previousDate,
                    followingDate): 
                    iDataPoint = newsEle.getPointFrom(iTime)
                    accumlatedSentimentalScore += iDataPoint.sentimentalScore
                carNewsDataPoints.append(
                    CarsNewsDataPoint(
                        carPoint,
                        accumlatedSentimentalScore)
                )                        
        except Exception as e: 
            print(F"Error: {gEleA.eleClass} and {gEleB.eleClass}")
            raise e
                
        return CarsNewsDataPoint.getGroupElement(carNewsDataPoints)
        
    
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
            if not isinstance(iPoint,CarsNewsDataPoint): 
                return False
            coordinates.add(iPoint.carN.coordinate)
        return len(coordinates) == 1
    
    @classmethod
    def getGroupElement(
        cls,
        points:list['DataPoint'])->CarsNewsElement: 
        return  CarsNewsElement(points)


    
class CarsNewsElement(GroupElement):
    
    def __init__(self,points:list[CarsNewsDataPoint]):
        self.element = points 
        
    @property
    def eleClass(self)->type[DataPoint]: 
        return CarsNewsDataPoint
    
    @property
    def element(self)->dict[str,CarsNewsDataPoint]:
        return self.__element
    
    @element.setter
    def element(self,val:list[CarsNewsDataPoint]): 
        validPoints = dict()
        for iPoint in val: 
            if iPoint.valid() and isinstance(iPoint,CarsNewsDataPoint):
                validPoints[iPoint.carN.coordinate] = iPoint
        self.__element = validPoints            
        
    
    def convertible(cls,targetClass:type[DataPoint])->bool:
        return False 
    
    def convertTo(self,targetClass:type[DataPoint])->'GroupElement':
        pass     
         
    @classmethod
    def getConvertResultClasses(cls)->list[DataPoint]:
        return []    
            

        
        
                 