from date_utils import DateRepresentation
from ..dataPoint import DataPoint,Element
from .NoneDataPoint import NoneDataPoint        
from collection_vistor import Vistor

class NewsNewsDataPoint(DataPoint): 
    
    
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
    def correspondingGroupElement(self)->Element:
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
    def getGroupElement(cls, points:list['NewsNewsDataPoint']):
        return NewsElement(points)

    def getTypeGroupElement(cls)->type[Element]:
        return NewsElement
    
    

class NewsElement(Element):
    def __init__(self,points:list[NewsNewsDataPoint]):
        self.inList = points        
    
    @property
    def type(self)->type[DataPoint]: 
        return NewsNewsDataPoint
    
    @property
    def inList(self)->dict[int,NewsNewsDataPoint]:
        return self.__element
    
    @inList.setter
    def inList(self,val:list[NewsNewsDataPoint]): 
        validPoints = dict()
        for iPoint in val: 
            if isinstance(iPoint,NewsNewsDataPoint):
                if iPoint.valid():
                    validPoints[iPoint.__hash__()]=(iPoint)
        self.__element = validPoints


    
    def acceptVistor(self,v:Vistor):
        return v.visitNewsElement(self)
    
    def acceptOutVistor(
        self,
        v:Vistor,
        dest:str): 
        return v.visitOutNewsElement(self,dest)

                
    @classmethod
    def convertible(cls,targetClass:type[DataPoint])->bool:
        return False 
    
    
    def convertTo(self,targetClass:type[DataPoint])->'Element':
        pass     
    
    def getPointFrom(self,date:DateRepresentation)->NewsNewsDataPoint: 
        hashStr = ("14" 
                    +str(date).replace('-',''))
        return self.inList.get(int(hashStr),NoneDataPoint)
    
    
    @classmethod
    def getConvertResultClasses(cls)->list[DataPoint]:
        return []        
