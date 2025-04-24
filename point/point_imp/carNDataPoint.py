from ....date_utils import dateRepresentation
from ..data_point import DataPoint

class CarNDataPoint(DataPoint): 
    _enum = ['previousDate','followingDate','cumulativeAbnormalReturn','intervalN'] 
    
    def __init__(self,date,previousDate,followingDate,cumulativeAbnormalReturn,intervalN): 

        self.__date = dateRepresentation.DateRepresentation(date)
        self.__previousDate = dateRepresentation.DateRepresentation(previousDate)
        self.__followingDate = dateRepresentation.DateRepresentation(followingDate)
        self.__cumulativeAbnormalReturn = cumulativeAbnormalReturn
        self.__intervalN = intervalN

    
    @property
    def date(self)->dateRepresentation.DateRepresentation:
        return self.__date
    # @date.setter
    # def date(self,date): 
    #     self.__date = dateRepresentation.DateRepresentation.getInstance(date)
            
    @property
    def previousDate(self)->dateRepresentation.DateRepresentation:
        return self.__previousDate    
    # @previousDate.setter
    # def previousDate(self,date): 
    #     self.__previousDate = dateRepresentation.DateRepresentation(date)
        
    @property
    def followingDate(self)->dateRepresentation.DateRepresentation: 
        return self.__followingDate        
    # @followingDate.setter
    # def followingDate(self,date):
    #     self.__followingDate = dateRepresentation.DateRepresentation(date)

    @property
    def cumulativeAbnormalReturn(self)->float: 
        return self.__cumulativeAbnormalReturn

    
    @property
    def mapping(self)->map:                         
        mAttri = self.getEnum()
        mVal = [self.__previousDate,self.__followingDate,self.__cumulativeAbnormalReturn,self.__intervalN] 
        return dict(zip(mAttri,mVal))
        
    @property
    def coordinate(self)->str:
        return self.getCoordinateFrom(self.__previousDate,self.__date,self.__followingDate)



    def getDataValueWithAttribute(self,attribute:str): 
        return self.mapping[attribute]
         
        
    def valid(self)->bool:  
        attributeStr = self.getEnum()[2]
        return  self.getDataValueWithAttribute(attributeStr) is not None 
    
    
    
    @classmethod
    def getCoordinateFrom(cls,previousDate:dateRepresentation.DateRepresentation,
                         carDate:dateRepresentation.DateRepresentation,
                         followingDate:dateRepresentation.DateRepresentation):
        return 'p'+previousDate.standardFormat+'c'+carDate.standardFormat+'f'+followingDate.standardFormat
        
    
    @classmethod
    def comparable(cls, *arg)->bool:
        preDateSet = set()
        folDateSet = set()        
        for carN in list(arg): 
            carN: CarNDataPoint
            preDateAttriStr = cls.getEnum()[0]
            follDateAttriStr = cls.getEnum()[1]
            preDateSet.add(carN.getDataValueWithAttribute(preDateAttriStr))
            folDateSet.add(carN.getDataValueWithAttribute(follDateAttriStr))
        return len(preDateSet) == 1 and len(folDateSet) == 1



    @classmethod
    def getEnum(cls):
        return cls._enum



    