from __future__ import annotations

from ...._date_utils import DateRepresentation
from ...base import DataPoint,Element     



class NewsDataPoint(DataPoint): 
    
    def __init__(
        self,
        date:DateRepresentation|str,
        siteAddress:str="",
        sentimentalScore:int|str|float=None
        ):
           
        self.date = date 
        self._siteAddress = siteAddress
        self.sentimentalScore = sentimentalScore

    def __hash__(self): 
        hashStr = ("14" 
                    +str(self.date).replace('-',''))
        return int(hashStr)
            
    @property
    def date(self)->DateRepresentation:
        return self._date
    
    @date.setter
    def date(self,val):
        self._date = DateRepresentation(val)
       
            
    @property
    def sentimentalScore(self)->float: 
        return self._sentimentalScore
    
    @sentimentalScore.setter
    def sentimentalScore(self,val):
        try: 
            floatScore = float(val)
            self._sentimentalScore = floatScore
        except:
            self._sentimentalScore = None

    
    def valid(self)->bool:
        return (DateRepresentation.isValidDateObj(self.date) 
                and isinstance(self.sentimentalScore,float))

    def toJson(self)->dict:
        return {
            "id": self.__hash__(),
            "type_name": self.__class__.__name__,
            "date": str(self.date),
            "siteAddress": self._siteAddress,
            "sentimentalScore": str(self.sentimentalScore)
        }
    @classmethod
    def correspondingGroupElement(cls)->type[NewsElement]:
        return NewsElement 
    
    @classmethod
    def getGroupElement(cls, points:list[NewsDataPoint])->NewsElement:
        return NewsElement(points)

    
    
class NewsElement(Element):
    def __init__(self,points:list[NewsDataPoint]=[]):
        self.dataPoints = points        
    
    @property
    def dataPoints(self)->list[NewsDataPoint]:
        return self._dataPoints
    
    @dataPoints.setter
    def dataPoints(self,val:list[NewsDataPoint]): 
        validPoints = []
        for iPoint in val: 
            if isinstance(iPoint,NewsDataPoint) and iPoint.valid():
                    validPoints.append(iPoint)
        self._dataPoints = validPoints



    @classmethod
    def getPointType(cls)->type[NewsDataPoint]:
        return NewsDataPoint    