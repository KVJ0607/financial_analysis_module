from date_utils import DateRepresentation
from ..dataPoint import DataPoint,GroupElement
from .NoneDataPoint import NoneDataPoint        

class NewsNewsDataPoint(DataPoint): 
    
    
    def __init__(self,date,siteAddress:str,sentimentalScore:int|str|float):   
        self.date = date 
        self.__siteAddress = siteAddress
        self.sentimentalScore = sentimentalScore

    def __hash__(self): 
        hashStr = ("14" 
                    +self.date.standardFormatWithoutDash)
        return int(hashStr)
            
    @property
    def date(self)->DateRepresentation:
        return self.__date
    
    @date.setter
    def date(self,val):
        self.__date = DateRepresentation(val)

    @property
    def correspondingGroupElement(self)->GroupElement:
        return NewsNewsElement        
            
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

    @property
    def coordinate(self)->str: 
        return self.date.standardFormat
    
    def valid(self):
        return (DateRepresentation.isValid(self.date) 
                and isinstance(self.sentimentalScore,float))
    
    @classmethod
    def getGroupElement(cls, points:list['NewsNewsDataPoint']):
        return NewsNewsElement(points)

    def getTypeGroupElement(cls)->type[GroupElement]:
        return NewsNewsElement
    
    

class NewsNewsElement(GroupElement):
    def __init__(self,points:list[NewsNewsDataPoint]):
        self.element = points        
    
    @property
    def eleClass(self)->type[DataPoint]: 
        return NewsNewsDataPoint
    
    @property
    def element(self)->dict[int,NewsNewsDataPoint]:
        return self.__element
    
    @element.setter
    def element(self,val:list[NewsNewsDataPoint]): 
        validPoints = dict()
        for iPoint in val: 
            if isinstance(iPoint,NewsNewsDataPoint):
                if iPoint.valid():
                    validPoints[iPoint.__hash__()]=(iPoint)
        self.__element = validPoints
                

    def convertible(self,targetClass:type[DataPoint])->bool:
        return False 
    
    
    def convertTo(self,targetClass:type[DataPoint])->'GroupElement':
        pass     
    
    def getPointFrom(self,date:DateRepresentation)->NewsNewsDataPoint: 
        hashStr = ("14" 
                    +date.standardFormatWithoutDash)
        return self.element.get(int(hashStr),NoneDataPoint)
    
    
        
