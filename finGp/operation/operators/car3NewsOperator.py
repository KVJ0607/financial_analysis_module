   
from __future__ import annotations

from ..operator import Operator
from ...element import Element,Car3Element,NewsElement,NewsDataPoint,PricingElement,Car3NewsElement,Car3NewsDataPoint
from ..._date_utils import DateRepresentation
from ...group import SetOps

class Car3NewsOperator(Operator): 

    @classmethod
    def getProductClass(cls)->type[Car3NewsElement]:
        return Car3NewsElement         
                        
            
        
    
    @classmethod
    def getOperands(cls)->set: 
        return set([Car3Element,NewsElement])
        
    
    
    @classmethod
    def dot(
        cls,
        gEleA:Element,
        gEleB:Element) -> Element:                        
        carEle:Car3Element = None 
        newsEle:NewsElement = None
                
        if (type(gEleA) == Car3Element
            and type(gEleB) == NewsElement): 
            carEle = gEleA 
            newsEle = gEleB
        elif (type(gEleB) == Car3Element
            and type(gEleA) == NewsElement): 
            carEle = gEleB
            newsEle = gEleA
        else: 
            raise TypeError(f"""{gEleA} and {gEleB}
                            are of type {type[gEleA]}
                            and {type[gEleB]}, but not 
                            {Car3Element} and {NewsElement}""")
        
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
                Car3NewsDataPoint(
                    carPoint,
                    accumlatedSentimentalScore)
            )                        
                
        return Car3NewsDataPoint.getGroupElement(carNewsDataPoints)
        
