from __future__ import annotations


from date_utils import DateRepresentation
from point.dataPoint import DataPoint,Element
from collection_vistor import Vistor

        
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
        hashStr = "10"+str(self.date).replace('-','')
        return int(hashStr)

    @property
    def date(self)->DateRepresentation: 
        return self.__date
  
    @property
    def correspondingGroupElement(self)->Element:
        return NoneElement        

    
    def valid():  
        return False                               
    
    
    @classmethod
    def getGroupElement(cls)->NoneElement:
        return NoneElement()

    def getTypeGroupElement(cls)->type[Element]:
        return NoneElement



class NoneElement(Element):    
    def __init__(self):
        self.__done = True         
    
    @property
    def type(self)->type[DataPoint]: 
        return NoneDataPoint
    
    @property
    def inList(self)->dict[int,NoneDataPoint]:
        return dict()


    def acceptVistor(self,v:Vistor):
        return v.visitNoneElement(self)

    def acceptOutVistor(
        self,
        v:Vistor,
        dest:str): 
        return v.visitOutNoneElement(self,dest)        
        
    @classmethod
    def convertible(cls,targetClass:type[DataPoint])->bool:
        return False 
    
    
    def convertTo(self,targetClass:type[DataPoint])->'Element':
        pass     
    
    @classmethod
    def getConvertResultClasses(cls)->list[DataPoint]:
        return []    