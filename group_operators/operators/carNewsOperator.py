   
from __future__ import annotations

# import matplotlib.pyplot as plt
# import numpy as np


from ..operator import CollectionOperator
from element_of_group import DataPoint,Element,NoneDataPoint,CarNDataPoint,CarNElement,NewsElement,PricingElement
from date_utils import DateRepresentation

class CarNewsOperator(CollectionOperator): 

    @property
    def productClass(self)->type[Element]:
        return CarsNewsElement         

    @classmethod
    def match(
        cls,
        classA:type[Element],
        classB:type[Element])->bool:
        eSignature = set([classA,classB])
        for iSignature in cls.signatures(): 
            if iSignature == eSignature: 
                return True
        return False
        
    
    @classmethod
    def dot(
        cls,
        gEleA:Element,
        gEleB:Element,
        )->Element: 
        eSignature = set([type(gEleA),type(gEleB)])    
        for iSignature in cls.signatures():
            if iSignature == eSignature: 
                if eSignature == set([CarNElement,NewsElement]):
                    return cls.__defaultOperator(gEleA,gEleB)  
                elif eSignature == set([PricingElement,NewsElement]):
                    return cls.__pricingOperator(gEleA,gEleB)
                
            
        
    
    @classmethod
    def signatures(cls)->list[set]: 
        signatures = []
        signatures.append(set([CarNElement,NewsElement]))
        signatures.append(set([PricingElement,NewsElement]))
        return signatures
    
    
    @classmethod
    def __defaultOperator(
        cls,
        gEleA:Element,
        gEleB:Element) -> Element:                        
        carEle:CarNElement = None 
        newsEle:NewsElement = None
                
        if (type(gEleA) == CarNElement
            and type(gEleB) == NewsElement): 
            carEle = gEleA 
            newsEle = gEleB
        elif (type(gEleB) == CarNElement
            and type(gEleA) == NewsElement): 
            carEle = gEleB
            newsEle = gEleA
        else: 
            raise TypeError(f"""{gEleA} and {gEleB}
                            are of type {type[gEleA]}
                            and {type[gEleB]}, but not 
                            {CarNElement} and {NewsElement}""")
        
        
        carNewsDataPoints = []
        try:
            for carHash,carPoint in carEle.inDict.items():                 
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
            print(F"Error: {type(gEleA)} and {type(gEleB)}")
            raise e
                
        return CarsNewsDataPoint.getGroupElement(carNewsDataPoints)
        
    
    @classmethod
    def __pricingOperator(
        cls,
        gEleA:Element,
        gEleB:Element) -> Element:         
        if type(gEleA) == PricingElement: 
            return cls.__defaultOperator(
                gEleA.convertTo(CarNElement),
                gEleB)
        else: 
            return cls.__defaultOperator(
                gEleB.convertTo(CarNElement),
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
        points:list[CarsNewsDataPoint])->CarsNewsElement: 
        return  CarsNewsElement(points)


    
class CarsNewsElement(Element):
    
    def __init__(self,points:list[CarsNewsDataPoint]):
        self.inDict = points 
        
    @property
    def pointType(self)->type[DataPoint]: 
        return CarsNewsDataPoint
    
    @property
    def inDict(self)->dict[str,CarsNewsDataPoint]:
        return self.__element
    
    @inDict.setter
    def inDict(self,val:list[CarsNewsDataPoint]): 
        validPoints = dict()
        for iPoint in val: 
            if iPoint.valid() and isinstance(iPoint,CarsNewsDataPoint):
                validPoints[iPoint.__hash__()] = iPoint
        self.__element = validPoints            


    def acceptVistor(self,v:Vistor):
        return v.visitCarsNewsElement(self)  

   
    def acceptOutVistor(
        self,
        v:Vistor,
        dest:str): 
        return v.visitOutCarsNewsElement(self,dest)        
        

    @classmethod
    def convertible(cls,targetClass:type[Element])->bool:
        return False 
    
    def convertTo(self,targetClass:type[Element])->'Element':
        pass     
         
    @classmethod
    def getConveribleClasses(cls)->list[DataPoint]:
        return []    
            

        
        
                 