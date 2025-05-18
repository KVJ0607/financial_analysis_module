from __future__ import annotations

from ...date_utils import DateRepresentation
from ..base import DataPointBase,ElementBase     
from ..setopsMixin import SetOpsMixin
from ..visitorMixin import VisitorMixin

class NewsDataPoint(DataPointBase): 
    
    def __init__(self,date,siteAddress:str,sentimentalScore:int|str|float):   
        self.date = date 
        self.__siteAddress = siteAddress
        self.sentimentalScore = sentimentalScore

    def __hash__(self): 
        hashStr = ("14" 
                    +str(self.date).replace('-',''))
        return int(hashStr)
            
    @property
    def date(self)->DateRepresentation:
        return self.__date
    
    @date.setter
    def date(self,val):
        self.__date = DateRepresentation(val)

    @property
    def correspondingGroupElement(self)->type[ElementBase]:
        return NewsElement        
            
    @property
    def sentimentalScore(self)->float: 
        return self.__sentimentalScore
    
    @sentimentalScore.setter
    def sentimentalScore(self,val):
        try: 
            floatScore = float(val)
            self.__sentimentalScore = floatScore
        except:
            self.__sentimentalScore = None

    
    def valid(self):
        return (DateRepresentation.isValid(self.date) 
                and isinstance(self.sentimentalScore,float))
    
    @classmethod
    def getGroupElement(cls, points:list[NewsDataPoint])->NewsElement:
        return NewsElement(points)

    def getTypeGroupElement(cls)->type[ElementBase]:
        return NewsElement
    
class NewsVisitor(VisitorMixin):
    def acceptVisitor(self,v):
        return v.visitNewsElement(self)
    
    def acceptOutVisitor(
        self,
        v,
        dest:str): 
        return v.visitOutNewsElement(self,dest)
    
class NewsElement(ElementBase,SetOpsMixin,NewsVisitor):
    def __init__(self,points:list[NewsDataPoint]=[]):
        self.dataPoints = points        
    
    @property
    def pointType(self): return NewsDataPoint
    
    @property
    def dataPoints(self)->dict[int,NewsDataPoint]:
        return self._dataPoints
    
    @dataPoints.setter
    def dataPoints(self,val:list[NewsDataPoint]): 
        validPoints = []
        for iPoint in val: 
            if isinstance(iPoint,NewsDataPoint) and iPoint.valid():
                    validPoints.append(iPoint)
        self._dataPoints = validPoints

        
    

    