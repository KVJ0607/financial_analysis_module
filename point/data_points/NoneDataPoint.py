from __future__ import annotations


from date_utils import DateRepresentation
from point.dataPoint import DataPoint,GroupElement

        
class NoneDataPoint(DataPoint): 
    '''
    A special class that represent the absent of market day 
    '''
    def __init__(self,date = None):
        if date == None: 
            self.__date = DateRepresentation.getNullInstance()
        else:
            self.__date = DateRepresentation(date)
        
    def __hash__(self): 
        hashStr = "10"+self.date.standardFormatWithoutDash
        return int(hashStr)

    @property
    def date(self)->DateRepresentation: 
        return self.__date
  
    @property
    def correspondingGroupElement(self)->GroupElement:
        return NoneElement        

    @property
    def coordinate(self):
        '''Special Index saved for NoneDataPoint'''
        return 'NoneDataPoint'+self.date.dateTimeDate
    
    def valid():  
        return False                               
    
    
    @classmethod
    def getGroupElement(cls)->NoneElement:
        return NoneElement()

    def getTypeGroupElement(cls)->type[GroupElement]:
        return NoneElement

class NoneElement(GroupElement):    
    def __init__(self):
        self.__done = True         
    
    @property
    def eleClass(self)->type[DataPoint]: 
        return NoneDataPoint
    
    @property
    def element(self)->dict[int,NoneDataPoint]:
        return dict()
    
    @classmethod
    def convertible(cls,targetClass:type[DataPoint])->bool:
        return False 
    
    
    def convertTo(self,targetClass:type[DataPoint])->'GroupElement':
        pass     
    
    @classmethod
    def getConvertResultClasses(cls)->list[DataPoint]:
        return []    