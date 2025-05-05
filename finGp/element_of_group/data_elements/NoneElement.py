from __future__ import annotations


from ...date_utils import DateRepresentation
from ...element_of_group.element import DataPoint,Element

        
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
    def correspondingGroupElement(self)->type[Element]:
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
    def pointType(self)->type[DataPoint]: 
        return NoneDataPoint
    
    @property
    def inDict(self)->dict[int,NoneDataPoint]:
        return dict()


    def acceptVistor(self,v):
        return v.visitNoneElement(self)

    def acceptOutVistor(
        self,
        v,
        dest:str): 
        return v.visitOutNoneElement(self,dest)        
        
    @classmethod
    def convertible(cls,targetClass:type[Element])->bool:
        return False 
    
    
    def convertTo(self,targetClass:type[Element])->Element:
        pass     
    
    @classmethod
    def getConveribleClasses(cls)->list[type[Element]]:
        return []    