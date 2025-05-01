from date_utils import DateRepresentation
from point.dataPoint import DataPoint,GroupElement

class CarNDataPoint(DataPoint):     
    def __init__(self,date,previousDate,followingDate,cumulativeAbnormalReturn,intervalN): 

        self.__date = DateRepresentation(date)
        self.__previousDate = DateRepresentation(previousDate)
        self.__followingDate = DateRepresentation(followingDate)
        self.__cumulativeAbnormalReturn = cumulativeAbnormalReturn
        self.__intervalN = intervalN

    
    @property
    def date(self)->DateRepresentation:
        return self.__date
            
    @property
    def previousDate(self)->DateRepresentation:
        return self.__previousDate    
        
    @property
    def followingDate(self)->DateRepresentation: 
        return self.__followingDate        
    
    @property
    def cumulativeAbnormalReturn(self)->float: 
        return self.__cumulativeAbnormalReturn

    @property
    def intervalN(self)->int: 
        return self.__intervalN
        
    @property
    def coordinate(self)->str:
        return self.getCoordinateFrom(self.__previousDate,self.__date,self.__followingDate)
         
        
    def valid(self)->bool:  
        validA = DateRepresentation.isValid(self.__date)
        validB = DateRepresentation.isValid(self.__previousDate)
        validC = DateRepresentation.isValid(self.__followingDate)
        validD = isinstance(self.__cumulativeAbnormalReturn,(int,float))
        validE = (isinstance(self.__intervalN,int) 
                    and self.__intervalN > 2 
                    and self.__intervalN//2 == 1)
        
        if validA and validB and validC and validD and validE:
            return  True
        else:
            return False
    
    
    
    @classmethod
    def getCoordinateFrom(
        cls,
        previousDate:DateRepresentation,
        followingDate:DateRepresentation,
        intervlN:int):
        return ('p'+previousDate.standardFormat
                +'f'+followingDate.standardFormat 
                +'i'+str(intervlN))
        
    
    @classmethod
    def equivalent(cls, *arg)->bool:
        coordinates = set()
        
        for iCar in list(arg): 
            iCar: CarNDataPoint
            coordinates.add(cls.getCoordinateFrom(
                iCar.previousDate,
                iCar.followingDate,
                iCar.intervalN))
            
        return len(coordinates)==1



    @classmethod
    def getGroupElement(cls, points:list['CarNDataPoint']):
        return CarNElement(points)

            
class CarNElement(GroupElement):
    def __init__(self,points:list[CarNDataPoint]):
        self.element = points        
    
    @property
    def eleClass(self)->type[DataPoint]: 
        return CarNDataPoint
    
    @property
    def element(self)->list[CarNDataPoint]:
        return self.__element
    
    @element.setter
    def element(self,val:list[CarNDataPoint]): 
        validPoints = []
        for iPoint in val: 
            if iPoint.valid() and isinstance(iPoint,CarNDataPoint):
                validPoints.append(iPoint)
        self.__element = validPoints
            
            
    
    
    