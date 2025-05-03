from date_utils import DateRepresentation
from ..dataPoint import DataPoint,GroupElement
from .carNDataPoint import CarNDataPoint,CarNElement
from .NoneDataPoint import NoneDataPoint

    
class PricingDataPoint(DataPoint): 
    def __init__(self,date,open,high,low,close,adjClose,volume):               
        self.date = date
        self.__open = open 
        self.__high = high 
        self.__low = low
        self.__close = close 
        self.__adjClose = adjClose
        self.__volume = volume
            
        
    

    def __hash__(self): 
        hashStr = ("12"+self.date.standardFormatWithoutDash)
        return int(hashStr)

        

    @property
    def date(self)->DateRepresentation:
        return self.__date
    
    @date.setter
    def date(self,val):
        self.__date = DateRepresentation(val)

    @property
    def correspondingGroupElement(self)->GroupElement:
        return PricingElement        
    
    @property
    def adjClose(self)->float:
        try:
            return float(self.__adjClose) 
        except: 
            return None
    
    @property
    def coordinate(self)->str:
         return self.date.standardFormat
    
    def valid(self)->bool:   
        if not DateRepresentation.isValid(self.date): 
            return False
                
        if (self.adjClose is None) or (not isinstance(self.adjClose,float)): 
            return False
        
        return True
    
  
    @classmethod
    def getGroupElement(cls,points:list['DataPoint'])->GroupElement: 
        return PricingElement(points)  
        
    def getTypeGroupElement(cls)->type[GroupElement]:
        return PricingElement
    
    

class PricingElement(GroupElement):
    def __init__(self,points:list[PricingDataPoint]):
        self.element = points 
    
    @property    
    def eleClass(self)->type[DataPoint]: 
        return PricingDataPoint  
         
    @property
    def element(self)->dict[int,PricingDataPoint]: 
        return self.__element
    
    @element.setter
    def element(self,val:list[DataPoint]):
        validPoints = dict()
        for iPoint in val: 
            if isinstance(iPoint,PricingDataPoint):
                if iPoint.valid():
                    validPoints[iPoint.__hash__()]=(iPoint)
        self.__element = validPoints                     
    
    @property
    def dates(self)->list[DateRepresentation]:
        thisDates = []
        for iEle in self.element.values(): 
            thisDates.append(iEle.date)
        return thisDates

    def convertible(self,targetClass:type[DataPoint])->bool:
        if targetClass == CarNDataPoint:
            return True
        else: 
            return False
    
    
    def convertTo(self,targetClass:type[DataPoint])->'GroupElement':
        if targetClass == CarNDataPoint:
            return self.__convertToCarNColl()  
        
        
    def __convertToCarNColl(self,nDay:int=3)->GroupElement|CarNElement: 
        if nDay//2 == 0: 
            raise ValueError("nDay should be an odd number")
        if nDay < 1: 
            raise ValueError("nDay should be a positive number")
        nDay = (nDay-1)/2             
        
        dateList = sorted(self.dates)
        
        carNPoints:list = [] 
        for iDay in DateRepresentation.getDateRange(dateList[1],dateList[-1]):
            if iDay+nDay in dateList and iDay-nDay in dateList:
                lastPoint:PricingDataPoint = self.getPointFrom(iDay-nDay)
                nextPoint:PricingDataPoint = self.getPointFrom(iDay+nDay)
                if lastPoint.valid() and nextPoint.valid():
                    carNPoints.append(CarNDataPoint(
                        iDay,
                        iDay-nDay,
                        iDay+nDay,
                        (nextPoint.adjClose-lastPoint.adjClose)/lastPoint.adjClose,
                        nDay)
                    )
        return CarNElement(carNPoints)

    
    def getPointFrom(self,date:DateRepresentation)->PricingDataPoint:
        hashStr = ("12"+date.standardFormatWithoutDash)        
        return self.element.get(int(hashStr),NoneDataPoint)    
    
    