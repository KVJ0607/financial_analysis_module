from date_utils import dateRepresentation 
from point.dataPoint import DataPoint


class HistoricalDataPoint(DataPoint): 
    '''Data wrapper of Market History on a specified date'''
    _enum = []
    def __init__(self,date,attributes:list,values:list,coreAttributes:list=[]):        
        self.__date = dateRepresentation.DateRepresentation.getInstance(date)
        self.__attributes = attributes
        self.__values = values 
        self.__coreAttributes = coreAttributes


    @property
    def date(self)->dateRepresentation.DateRepresentation:
        return self.__date

    @property                  
    def mapping(self)->map:
        return dict(zip(self.attributes,self.__values))
    
    @property
    def coordinate(self)->str:
        return self.date.standardFormat

    @property
    def attributes(self)->list[str]: 
        return self.__attributes

    @property
    def coreAttributes(self)->list[str]: 
        return self.__coreAttributes
    
    def getDataValueWithAttribute(self, attribute):
        return self.mapping[attribute]

    def valid(self)->bool:   
        if self.date is None: 
            return False
        for cAttribute in self.coreAttributes:        
            if self.attributesIsNone(cAttribute): 
                return False
        return True         
    
    def attributesIsNone(self,attribute)->bool: 
        return self.getDataValueWithAttribute(attribute) is None
    
    @classmethod
    def getCoordinateFrom(cls,date):
        return dateRepresentation.DateRepresentation.toStandardFormat(date)
    
                                            
    @classmethod
    def comparable(cls, *arg)->bool:
        compareSet = set()        
        for element in list(arg): 
            element:HistoricalDataPoint
            compareSet.add(element.date())            
        return len(compareSet) == 1
    
 

    
    
class PricingDataPoint(HistoricalDataPoint): 
    def __init__(self,date,open,high,low,close,adjClose,volume):        
        super().__init__(date,self.enum(),[open,high,low,close,adjClose,volume],['adjClose']) 
        
    @classmethod
    def enum(cls):
        return ['open','high','low','close','adjClose','volume']
    
class AdjClosedDataPoint(HistoricalDataPoint):
    def __init__(self,date,adjClose):        
        super().__init__(date,self.enum(),[adjClose],self.enum())        
    
    @classmethod
    def enum(cls):
        return ['adjClose']

        
class NewsNewsDataPoint(HistoricalDataPoint): 
    _enum = ['siteAddress','sentimentalScore']
    
    def __init__(self,date,siteAddress:str,sentimentalScore:int|str|float):   
        super().__init__(date,self.enum(),[siteAddress,sentimentalScore],self.enum()) 

    @classmethod
    def enum(cls):
        return ['siteAddress','sentimentalScore']
        
