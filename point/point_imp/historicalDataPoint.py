from date_utils import DateRepresentation
from ..dataPoint import DataPoint



class HistoricalDataPoint(DataPoint): 
    '''Data wrapper of Market History on a specified date'''
    _enum = []
    def __init__(self,date,attributes:list,values:list,coreAttributes:list=[]):        
        self.__date = DateRepresentation(date)
        self.__attributes = attributes
        self.__values = values 
        self.__coreAttributes = coreAttributes


    @property
    def date(self)->DateRepresentation:
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
    
    def getValueWithAttribute(self, attribute):
        return self.mapping[attribute]

    def valid(self)->bool:   
        if not DateRepresentation.isValid(self.date): 
            return False
        for cAttribute in self.coreAttributes:        
            cData = self.getValueWithAttribute(cAttribute)
            if (cData is None) or (not isinstance(cData,float)): 
                return False
        return True         
    

    
    @classmethod
    def getCoordinateFrom(cls,date):
        return DateRepresentation.toStandardFormat(date)
    
                                            
    @classmethod
    def equivalent(cls, *arg)->bool:
        compareSet = set()        
        for element in list(arg): 
            element:HistoricalDataPoint
            compareSet.add(element.date())            
        return len(compareSet) == 1
    
 

    
    
class PricingDataPoint(HistoricalDataPoint): 
    def __init__(self,date,open,high,low,close,adjClose,volume):       
        super().__init__(
            date,
            self.enum(),
            safeListConvertToType([open,high,low,close,adjClose,volume],float),
            [self.enum()[4]]) 
        
    @classmethod
    def enum(cls):
        return ['open','high','low','close','adjClose','volume']

    
    
    @property
    def adjClose(self)->float:
        return self.getValueWithAttribute(self.enum()[4])
    
    def valid(self)->bool:   
        if not DateRepresentation.isValid(self.date): 
            return False
                
        if (self.adjClose is None) or (not isinstance(self.adjClose,float)): 
            return False
        
        return True
        
        
    
class AdjClosedDataPoint(HistoricalDataPoint):
    def __init__(self,date,adjClose):        
        super().__init__(date,self.enum(),[float(adjClose)],self.enum())        
    
    @classmethod
    def enum(cls):
        return ['adjClose']

        
class NewsNewsDataPoint(HistoricalDataPoint): 
    _enum = ['siteAddress','sentimentalScore']
    
    def __init__(self,date,siteAddress:str,sentimentalScore:int|str|float):   
        super().__init__(date,self.enum(),[siteAddress,float(sentimentalScore)],[self.enum()[1]]) 

    @classmethod
    def enum(cls):
        return ['siteAddress','sentimentalScore']
        

def safeListConvertToType(value:list, type)->list: 
    '''Convert a list of value to a specific type'''
    if value is None: 
        return None
    if type == str: 
        safeList:list[str] = []
        for v in value: 
            try:                
                safeList.append(str(v))
            except ValueError: 
                safeList.append(v)
    elif type == int: 
        safeList:list[int] = []
        for v in value: 
            try:                
                safeList.append(int(v))
            except ValueError: 
                safeList.append(v)
    elif type == float: 
        safeList:list[float] = []
        for v in value: 
            try:                
                safeList.append(float(v))
            except ValueError: 
                safeList.append(v)                
    else:
        raise TypeError(f'Unsupported type {type}')
    return safeList