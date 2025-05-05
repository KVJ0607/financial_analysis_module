   
from __future__ import annotations


from ..operator import CollectionOperator
from ...element_of_group import Element,CarNElement,NewsElement,PricingElement,CarsNewsElement,CarsNewsDataPoint
from ...date_utils import DateRepresentation

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
            