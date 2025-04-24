
from datetime import date

from ..date_utils.dateRepresentation import DateRepresentation



class NullDateRepresentation(DateRepresentation):                 
    
    def __init__(self):
        pass 
    
    def __lt__(self,other):
        self._raiseComparisonError(other)
    def __le__(self,other):
        self._raiseComparisonError(other)                     
    def __gt__(self,other):
        self._raiseComparisonError(other)
    def __ge__(self,other):
        self._raiseComparisonError(other)
    def __eq__(self,other): 
        self._raiseComparisonError(other)               

    @property
    def standardFormat(self)->str:
        return '0001-01-01'
    
    @property
    def dateTimeDate(self)->date:
        return date(1,1,1)
    
        
    def isSupmiumDay(self)->bool:
        return False
        
    def changeToNextDay(self):
        pass                 
        
    def changeToPreviousDay(self):
        pass 

    def changeToPrevious_N_Day(self):
        pass 
        
    def changeToNext_N_Day(self):
        pass 
    

    def createPrevious_N_Day(self,integer_N:int)->'DateRepresentation':
        return NullDateRepresentation()
    
    def createNext_N_Day(self,integer_N:int)->'DateRepresentation':
        return NullDateRepresentation()        

       

    
    
        
            
           


    
    
    
    
    
    
    
        
        
    
    