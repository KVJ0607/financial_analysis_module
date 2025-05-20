   
from __future__ import annotations

from ...element.helper.non_generator.registry import Registry

from ..operator import Operator
from ...element import Element,CarNElement,NewsElement,NewsDataPoint,PricingElement,CarNewsElement,CarNewsDataPoint,SetOps
from ..._date_utils import DateRepresentation

class CarNewsOperator(Operator): 

    @classmethod
    def getProductClass(cls)->type[CarNewsElement]:
        return CarNewsElement         

    @classmethod
    def match(
        cls,
        classA:type[Element],
        classB:type[Element])->bool:
        eSignature = set([classA,classB])
        for iSignature in cls.getSignatures(): 
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
        for iSignature in cls.getSignatures():
            if iSignature == eSignature: 
                if eSignature == set([CarNElement,NewsElement]):
                    return cls._defaultOperator(gEleA,gEleB)  
                elif eSignature == set([PricingElement,NewsElement]):
                    return cls._pricingOperator(gEleA,gEleB)
                
            
        
    
    @classmethod
    def getSignatures(cls)->list[set]: 
        signatures = []
        signatures.append(set([CarNElement,NewsElement]))
        signatures.append(set([PricingElement,NewsElement]))
        return signatures
    
    
    @classmethod
    def _defaultOperator(
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
        
        newsInSet = SetOps(newsEle)
        indexedNews = newsInSet.index()
        
        carNewsDataPoints = []
        for carPoint in carEle.dataPoints:                 
            previousDate = carPoint.previousDate
            followingDate = carPoint.followingDate                 
            accumlatedSentimentalScore = 0                    
            for iTime in DateRepresentation.getDateRange(
                previousDate,
                followingDate): 
                dummyNews = NewsDataPoint(iTime)
                iDataPoint = indexedNews.get(hash(dummyNews),None)
                if iDataPoint:
                    accumlatedSentimentalScore += iDataPoint.sentimentalScore
            carNewsDataPoints.append(
                CarNewsDataPoint(
                    carPoint,
                    accumlatedSentimentalScore)
            )                        
                
        return CarNewsDataPoint.getGroupElement(carNewsDataPoints)
        
    
    @classmethod
    def _pricingOperator(
        cls,
        gEleA:Element,
        gEleB:Element) -> Element:         
        if type(gEleA) == PricingElement: 
            return cls._defaultOperator(
                gEleA.convertTo(CarNElement),
                gEleB)
        else: 
            return cls._defaultOperator(
                gEleB.convertTo(CarNElement),
                gEleA)            

req1 = Registry.makeElementRequirements({CarNElement,NewsElement})            
req2 = Registry.makeElementRequirements({PricingElement,NewsElement})            

Registry.update(CarNewsElement,req1)
Registry.update(CarNewsElement,req2)