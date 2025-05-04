from __future__ import annotations

from date_utils import DateRepresentation
from point.dataPoint import DataPoint,GroupElement
from collection_vistor import Vistor

class CarNDataPoint(DataPoint):     
    def __init__(self,date,previousDate,followingDate,cumulativeAbnormalReturn,intervalN): 

        self.__date = DateRepresentation(date)
        self.__previousDate = DateRepresentation(previousDate)
        self.__followingDate = DateRepresentation(followingDate)
        self.__cumulativeAbnormalReturn = cumulativeAbnormalReturn
        self.__intervalN = intervalN

    def __hash__(self): 
        hashStr = ("13" 
                    +str(self.previousDate).replace('-','')
                    +str(self.followingDate).replace('-','')
                    +self.intervalN)
        return int(hashStr)
        
    @property
    def date(self)->DateRepresentation:
        return self.__date

    @property
    def correspondingGroupElement(self)->GroupElement:
        return CarNElement        
                
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
    def getGroupElement(cls, points:list['CarNDataPoint']):
        return CarNElement(points)

    @classmethod
    def getTypeGroupElement(cls)->type[GroupElement]:
        return CarNElement 

            
class CarNElement(GroupElement):
    def __init__(self,points:list[CarNDataPoint]):
        self.element = points        
    
    @property
    def eleClass(self)->type[DataPoint]: 
        return CarNDataPoint
    
    @property
    def element(self)->dict[int,CarNDataPoint]:
        return self.__element
    
    @element.setter
    def element(self,val:list[CarNDataPoint]): 
        validPoints = dict()
        for iPoint in val: 
            if isinstance(iPoint,CarNDataPoint):
                if iPoint.valid():
                    validPoints[iPoint.__hash__()]=(validPoints)
        self.__element = validPoints


    
    def acceptVistor(self,v:Vistor):
        return v.visitCarNElement(self)            

    def acceptOutVistor(
        self,
        v:Vistor,
        dest:str): 
        return v.visitOutCarNElement(self,dest)
            
    @classmethod
    def convertible(cls,targetClass:type[DataPoint])->bool:
        return False 
    
    
    def convertTo(self,targetClass:type[DataPoint])->'GroupElement':
        pass     
    
    @classmethod
    def getConvertResultClasses(cls)->list[DataPoint]:
        return []
            
    
    